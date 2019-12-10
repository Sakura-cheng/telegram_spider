from telegram import main
import asyncio
import time
from sql_util import *
import json
import threading


async def run(phone, phone_id, category):
    try:
        change_status(phone_id, status=0)
        await main(phone, category)
    except Exception as e:
        print(e)
        error = json.loads(e.__str__())
        error_code = error["error_code"]
        msg = error["msg"]
        print(str(phone) + ": " + msg)
        # 修改数据库中状态
        change_status(phone_id, status=error_code)


async def create_task(event_loop):
    while True:
        time.sleep(5)
        # 从数据库中获得手机号
        category = 2
        phone, phone_id = get_phone(category)
        if phone is None:
            continue
        print("开始监听" + str(phone) + "...")

        # 添加任务进loop循环
        asyncio.run_coroutine_threadsafe(run(phone, phone_id, category), event_loop)


def start_loop(loop):
    #  运行事件循环， loop作为参数
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    thread_loop = asyncio.new_event_loop()  # 创建事件循环
    run_loop_thread = threading.Thread(target=start_loop, args=(thread_loop,))  # 新起线程运行事件循环, 防止阻塞主线程
    run_loop_thread.start()  # 运行线程，即运行协程事件循环

    main_loop = asyncio.new_event_loop()
    main_loop.run_until_complete(create_task(thread_loop))  # 主线程负责create coroutine object
