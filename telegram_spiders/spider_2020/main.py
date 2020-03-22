import asyncio
import time

from telegram import main
import json
from sql_util import get_phone, change_status
from message_util import get_phone_test, cancel_all_recv
from config import message_token
from check_util import check_main
from myLogger import log_main


def run(phone, category):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(phone, category))
    loop.close()


def loop_for_next_try():
    n = 0
    while True:
        n += 1
        print('------第' + str(n) + '次------')
        log_main.logger.info('------第' + str(n) + '次------')
        time.sleep(5)
        # 手动输入手机号
        # phone = input("请输入手机号\n")

        # 从数据库中获得手机号
        category = 1
        # phone, phone_id = get_phone(category)

        # 从接码平台获取手机号
        print('从接码平台获取手机号...')
        try:
            cancel_all_recv(message_token)
            status, phone = get_phone_test(message_token)
        except Exception as e:
            print(e)
            continue

        if status != '1':
            print("手机号获取失败...")
            log_main.logger.error(str(phone) + "手机号获取失败...")
            continue
        try:

            # 先判断该phone是否注册过
            # if not check_main('8617121240943', phone):
            #     print('该手机号未注册')
            #     change_status(phone_id, status=404)
            # else:
            run('86' + phone, category)
            # change_status(phone_id, status=1)
        except RuntimeError as e:
            print(e)
            log_main.logger.error(str(phone) + e.__str__())
            # error = json.loads(e.__str__())
            # error_code = error["error_code"]
            # msg = error["msg"]
            # print(msg)
            # 修改数据库中状态
            # change_status(phone_id, status=error_code)
        except Exception as e:
            print(e)
            log_main.logger.error(str(phone) + e.__str__())


if __name__ == '__main__':
    loop_for_next_try()
