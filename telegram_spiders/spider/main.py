import asyncio
import time

from telegram import main
import json
from sql_util import get_phone, change_status


def run(phone, category):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(phone, category))


def loop_for_next_try():
    while True:
        time.sleep(5)
        # 手动输入手机号
        # phone = input("请输入手机号\n")

        # 从数据库中获得手机号
        category = 1
        phone, phone_id = get_phone(category)
        if phone is None:
            print("没有待测的手机号...")
            continue
        try:
            run(phone, category)
            change_status(phone_id, status=1)
        except Exception as e:
            error = json.loads(e.__str__())
            error_code = error["error_code"]
            msg = error["msg"]
            print(msg)
            # 修改数据库中状态
            change_status(phone_id, status=error_code)


if __name__ == '__main__':
    loop_for_next_try()
