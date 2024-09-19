import concurrent
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List

from pymongo import MongoClient

from sais.autotrain.dataservice.config.const import LOGGER_NAME
from sais.autotrain.dataservice.model.data_model import Coordinate

logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(level=logging.INFO)

MONGO_URL = f'mongodb://{os.getenv("MONGO_USER", "root")}:{os.getenv("MONGO_PASSWORD", "yourPassword")}@{os.getenv("MONGO_HOST", "localhost")}:{os.getenv("MONGO_PORT", 8087)}'


def query_nwp_mongo(src: str, start_time: str, period_interval: int, period: int, start_hour: int, end_hour: int,
              forecast_interval: int, coords: list[Coordinate], vars: list[str], workers: int):
    query_start_time = time.time()  # 记录查询开始时间
    # 解析请求参数
    start_time = datetime.strptime(start_time, "%y%m%d%H")
    # 所有起报时间点
    forcast_start_times = []
    # 所有预报时间点
    forcast_times = []
    # 预报步长
    steps = []
    # forcast_time 按月分组
    month_groups = {}
    # 发布时次
    for i in range(period):
        forcast_start_time = start_time + timedelta(hours=i * period_interval)
        # logger.info(f'forcast_start_time: {forcast_start_time}')
        forcast_start_time_str = forcast_start_time.strftime("%Y-%m-%d %H:%M:%S")
        forcast_start_times.append(forcast_start_time_str)
        # 记录到月分组中
        month_key = forcast_start_time.strftime('%Y%m')
        if month_key not in month_groups:
            month_groups[month_key] = []
        month_groups[month_key].append(forcast_start_time_str)

        for hour in range(start_hour, end_hour + 1, forecast_interval):
            current_step = timedelta(hours=hour)
            forcast_time = forcast_start_time + current_step
            # logger.info(f'forcast_time: {forcast_time}')
            forcast_times.append(forcast_time.strftime("%Y-%m-%d %H:%M:%S"))

            # 格式化时间步长
            formatted_step = f"P{current_step.days}DT{current_step.seconds // 3600}H{(current_step.seconds // 60) % 60}M{current_step.seconds % 60}S"
            steps.append(formatted_step)
            # logger.info(f'forcast_start_times: {forcast_start_times}')
        # logger.info(f'forcast_times: {forcast_times}')
    result = query_mongo_multi_thread(workers, src, month_groups, steps, vars, coords)
    all_end_time = time.time()  # 记录查询结束时间
    all_execution_time = all_end_time - query_start_time
    logger.info(f"总耗时: {all_execution_time} 秒, 总数量：{len(result) if result else 0}")
    return result


def run_query(db: MongoClient, src: str, month_item: dict, forcast_times: list[str], steps: list[str], vars: list[str],
              coords: List[Coordinate]):
    query_conditions = []

    # 四舍五入经纬度到小数点后一位
    rounded_coords = [
        {"req_lat": round(coord.req_lat, 1), "req_lon": round(coord.req_lon, 1)}
        for coord in coords
    ]
    query_conditions.append({
        "src": src,
        "time": {"$in": forcast_times},
        "latitude": {"$in": [coord["req_lat"] for coord in rounded_coords]},
        "longitude": {"$in": [coord["req_lon"] for coord in rounded_coords]},
        "step": {"$in": steps},
        "$and": [{var: {"$exists": True}} for var in vars]
    })
    collection = get_collection(db, src, month_item)
    vars_dict = {key: 1 for key in vars}
    query = {"$and": query_conditions}
    logger.info(f'query: {query_conditions}')
    query_results = collection.find(query, {
        "src": 1,
        "time": 1,
        "valid_time": 1,
        "step": 1,
        **vars_dict
    }).sort({
        "time": 1,
        "step": 1
    })
    return list(query_results)


def query_mongo_multi_thread(workers, src: str, month_group: dict, steps: list[str], vars: list[str], coords: List[Coordinate]):
    # 并发查询
    all_results = []
    client = MongoClient(MONGO_URL,
                         serverSelectionTimeoutMS=6000,
                         connectTimeoutMS=6000)
    db = client[os.getenv("MONGO_DB", "auto_train")]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_month = {
            executor.submit(run_query, db, src, month_key, month_group[month_key], steps, vars, coords): month_key
            for month_key in month_group
        }
        for future in concurrent.futures.as_completed(future_to_month):
            month_key = future_to_month[future]
            try:
                results = future.result()
                all_results.extend(results)
                # 对所有结果进行排序
                all_results.sort(key=lambda x: (x['time'], x['valid_time']))
            except Exception as exc:
                print(f'Error for month {month_key}: {exc}')

    return all_results


def get_collection(db, src, year_month):
    cname = f"nwp_{src.split('/')[0]}_{year_month}"
    logger.info(f'collection name: {cname}')
    return db[cname]


def get_year_month(dt):
    year_month = dt.strftime("%Y%m")
    return year_month
