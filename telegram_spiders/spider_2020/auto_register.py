import xml.etree.ElementTree as ET
import os
import subprocess
from message_util import get_phone_test, cancel_all_recv, get_code, add_black
from config import message_token
import asyncio
import time
import random

from telethon import TelegramClient
from telethon.sessions import StringSession

import config
import telegram
from save_util import *
from sql_util import *
from myLogger import log_register

# telegram的api_id和api_hash
api_id = config.api_id
api_hash = config.api_hash


def get_center_point(node):
    bounds = node.get("bounds")
    # [180,329][864,401]
    left = bounds.split('][')[0]
    right = bounds.split('][')[1]
    x = (int(right.split(',')[0]) + int(left.split(',')[0][1:])) // 2
    y = (int(right.split(',')[1][:-1]) + int(left.split(',')[1])) // 2
    return x, y


def adb_tap(t, path, index):
    '''
    模拟点击
    :param t:
    :param path:
    :param index:
    :return:
    '''
    node = t.findall(path)[index]
    x, y = get_center_point(node)
    os.system("adb shell input tap {} {}".format(str(x), str(y)))


def adb_input(t, path, index, content):
    '''
    模拟输入
    :param t: tree
    :param path: xpath规则
    :param index: node的index
    :param content: 输入的内容
    :return:
    '''
    node = t.findall(path)[index]
    text = node.get("text").replace(" ", "")
    x, y = get_center_point(node)
    os.system("adb shell input tap {} {}".format(str(x), str(y)))

    # 光标移动到末尾
    adb_key_event(123)
    for i in range(len(text)):
        adb_key_event(67)
    os.system("adb shell input text {}".format(content))


def adb_key_event(key):
    # 67 退格
    # 123 光标移动到末尾键
    os.system("adb shell input keyevent {}".format(key))


def get_xml(filename="ui"):
    os.system("adb shell uiautomator dump /sdcard/ui.xml")
    os.system("adb pull /sdcard/ui.xml ./{}.xml".format(filename))


def if_node(t, path, index):
    print(path)
    try:
        node = t.findall(path)[index]
        return True
    except Exception as e:
        print(e)
        return False


def try_login(phone):
    # 拉取xml
    get_xml()
    # 解析xml
    origin_tree = ET.parse("ui.xml")

    # 输入区号和手机号
    adb_input(origin_tree, ".//node[@class='android.widget.EditText']", 0, "86")
    adb_input(origin_tree, ".//node[@class='android.widget.EditText']", 1, phone)

    # 模拟点击
    adb_tap(origin_tree, ".//node[@class='android.widget.ImageView']", 0)

    # 确保进入输入验证码阶段
    while True:
        time.sleep(3)
        get_xml()
        tree = ET.parse("ui.xml")
        if if_node(tree, ".//node[@class='android.widget.EditText']", 0):
            break
        # 手机号被ban
        elif if_node(tree, ".//node[@text='This phone number is banned.']", 0):
            add_black(message_token, phone)
            auto_register_insert_phone("86" + phone, "ban")
            raise RuntimeError('{"error_code": 1, "msg": "被封禁的手机号码..."}')
        # 无效的手机号
        elif if_node(tree, ".//node[@text='Invalid phone number. Please check the number and try again.']", 0):
            auto_register_insert_phone("86" + phone, "can not use")
            raise RuntimeError('{"error_code": 1, "msg": "无效的手机号码..."}')
        # 其他错误
        elif if_node(tree, ".//node[@text='OK']", 0):
            raise RuntimeError('{"error_code": 1, "msg": "其他错误..."}')


def input_code(phone):
    # 从接码平台获取验证码
    code = get_code(phone)
    # code = input()

    # 拉取xml
    get_xml()
    # 判断结果
    code_tree = ET.parse("ui.xml")

    for i in range(len(code)):
        adb_input(code_tree, ".//node[@class='android.widget.EditText']", i, code[i])
    # adb_tap(origin_tree, ".//node[@class='android.widget.ImageView']", 0)
    time.sleep(3)

    while True:
        get_xml()
        tree = ET.parse("ui.xml")

        if if_node(tree, ".//node[@class='android.widget.EditText']", 0):
            # 设置姓名
            if set_name_flag():
                name = set_name()
                adb_input(tree, ".//node[@class='android.widget.EditText']", 0, name)
                name = set_name()
                adb_input(tree, ".//node[@class='android.widget.EditText']", 1, name)
            else:
                name = set_name()
                adb_input(tree, ".//node[@class='android.widget.EditText']", 0, name)
            # 点击
            adb_tap(tree, ".//node[@class='android.widget.ImageView']", -1)
            break
        # 验证码错误
        elif if_node(tree, ".//node[@text='Invalid code']", 0):
            log_register.logger.info("验证码错误")
            raise RuntimeError('{"error_code": 1, "msg": "验证码错误"}')
        # 若是已经注册过的不需要设置姓名直接进入会话主页面
        else:
            auto_register_insert_phone("86" + phone, "registered")
            log_register.logger.info("已经注册过的")
            # 若是注册过就爬取该账号的相关信息
            get_the_phone_info("86" + phone)
            raise RuntimeError('{"error_code": 1, "msg": "已经注册过的..."}')


def get_code_form_client():
    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.view.View']", 1)

    get_xml()
    tree = ET.parse("ui.xml")
    node = tree.findall(".//node[@class='android.view.View']")[-2]
    code = node.get("content-desc")

    # adb_tap(tree, ".//node[@class='android.view.View']", -2)
    #
    # get_xml()
    # tree = ET.parse("ui.xml")
    # adb_tap(tree, ".//node[@class='android.widget.FrameLayout']", -3)
    #
    # p = subprocess.Popen("adb shell am broadcast -a clipper.get", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                      shell=True)
    # result = p.communicate()
    # code = str(result[0])
    code = code.split("Login code: ")[1][:5]

    adb_key_event(4)

    return code


def logout():
    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.ImageView']", 0)

    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.TextView']", 9)

    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.ImageView']", 1)

    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.TextView']", 1)

    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.TextView']", -1)

    # 点击“开始聊天”
    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.TextView']", -2)


def install():
    os.system("adb install telegram.apk")

    # 启动
    os.system("adb connect 127.0.0.1:62001")
    os.system("adb shell am start -n org.telegram.messenger/org.telegram.ui.IntroActivity")
    # org.telegram.messenger

    # 检测是否启动成功
    while True:
        get_xml()
        tree = ET.parse("ui.xml")
        if if_node(tree, ".//node[@class='android.widget.TextView']", -1):
            break

    # 点击“开始聊天”
    get_xml()
    tree = ET.parse("ui.xml")
    adb_tap(tree, ".//node[@class='android.widget.TextView']", -1)

    # 安装后有时会弹出语言选择框
    # for i in range(5):
    #     print("检查是否有语言选择框")
    #     get_xml()
    #     tree = ET.parse("ui.xml")
    #     if if_node(tree, ".//node[@text='Choose your language']", 0):
    #         adb_tap(tree, ".//node[@class='android.widget.TextView']", -1)
    #         break

    # 检查是否出现输入框
    while True:
        print("检查是否有输入框输入电话")
        get_xml()
        tree = ET.parse("ui.xml")
        if if_node(tree, ".//node[@class='android.widget.EditText']", 0):
            break


def uninstall():
    os.system("adb connect 127.0.0.1:62001")
    os.system("adb uninstall org.telegram.messenger")


async def login(phone):
    '''
    登录telegram
    :return:
    '''
    login_flag = False

    # 自动登录
    session, not_use = get_session(phone=phone)
    if session:
        print("自动登录中...")
        client = TelegramClient(StringSession(session), api_id, api_hash)
    else:
        login_flag = True
        client = TelegramClient(StringSession(), api_id, api_hash)

    # 连接telegram服务
    try:
        print("连接telegram服务...")
        await client.connect()
    except OSError:
        raise RuntimeError('{"error_code": 500, "msg": "连接telegram服务失败..."}')

    # 手动输入验证码来登录
    if login_flag:
        print("请手动登录，等待验证码...")
        try:
            sent = await client.send_code_request(phone=phone, force_sms=True)
            print(sent)
        except Exception as e:
            print(e)
            raise RuntimeError('{"error_code": 501, "msg": "请求验证码失败..."}')

        time.sleep(1)
        # 从客户端获取验证码
        code = get_code_form_client()
        log_register.logger.info("验证码：" + code)

        try:
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            raise RuntimeError('{"error_code": 502, "msg": "请求登录失败..."}')

    # 判断是否登录成功
    if await client.is_user_authorized():
        # print(str(phone) + "登录成功！")
        log_register.logger.info(str(phone) + "登录成功！")
        # 保存session以便下次自动登录
        session = client.session.save()
        save_session_file(phone=phone, session=session)
        insert_session(phone=phone, session=session)
    else:
        # print("登录失败")
        log_register.logger.error("登录失败")
        # delete_session(phone)
    return client


async def login2(phone):
    '''
    已注册的账号
    :return:
    '''
    login_flag = False

    # 自动登录
    session, not_use = get_session_platform(phone=phone)
    if session:
        print("自动登录中...")
        client = TelegramClient(StringSession(session), api_id, api_hash)
    else:
        login_flag = True
        client = TelegramClient(StringSession(), api_id, api_hash)

    # 连接telegram服务
    try:
        print("连接telegram服务...")
        await client.connect()
    except OSError:
        raise RuntimeError('{"error_code": 500, "msg": "连接telegram服务失败..."}')

    # 手动输入验证码来登录
    if login_flag:
        print("请手动登录，等待验证码...")
        try:
            sent = await client.send_code_request(phone=phone, force_sms=True)
            print(sent)
        except Exception as e:
            print(e)
            raise RuntimeError('{"error_code": 501, "msg": "请求验证码失败..."}')

        time.sleep(1)
        # 从客户端获取验证码
        code = get_code_form_client()
        log_register.logger.info("验证码：" + code)

        try:
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            raise RuntimeError('{"error_code": 502, "msg": "请求登录失败..."}')

    # 判断是否登录成功
    if await client.is_user_authorized():
        # print(str(phone) + "登录成功！")
        log_register.logger.info(str(phone) + "登录成功！")
        # 保存session以便下次自动登录
        session = client.session.save()
        save_session_file(phone=phone, session=session)
        # 保存到platform
        insert_session_platform(phone=phone, session=session)
    else:
        # print("登录失败")
        log_register.logger.error("登录失败")
        # delete_session(phone)
    return client


def save_session(phone):
    loop = asyncio.get_event_loop()
    phone = "86{}".format(phone)
    try:
        log_register.logger.info(phone)
        # print(phone)
        loop.run_until_complete(login(phone))
    except Exception as e:
        print(e)
        raise e


def get_the_phone_info(phone):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_info(phone, 1))


async def get_info(phone, category):
    # 登录以获得client
    try:
        client = await login2(phone)
    except Exception as e:
        raise RuntimeError(e)

    if category == 1:
        await telegram.get_me_info(client)
        await telegram.get_contacts_info(client)
        await telegram.get_dialogs_info(client)
        await client.disconnect()
        # # 退出登录
        # await client.log_out()
        # # 删除session文件
        # delete_session_file(phone)


def set_name_flag():
    '''
    是否输入lastname
    :return:
    '''
    return random.randint(0, 1)


def set_name():
    '''
    随机名字
    :return:
    '''
    first_name = ['Aaron', 'Ben', 'Carl', 'Daniel', 'Edgar', 'Francis', 'Gabriel', 'Harrison', 'Ignativs', 'Jack',
                  'Abel', 'Benson', 'Cary', 'Dennis', 'Edward', 'Frank', 'Gaby', 'Hugo', 'Ivan', 'Jackson']
    name = random.choice(first_name)
    print(name)
    return name


def main(end):
    while True:
        start_time = time.time()
        uninstall()
        install()
        try:
            # 获取手机号
            log_register.logger.info('从接码平台获取手机号...')
            # print('从接码平台获取手机号...')
            cancel_all_recv(message_token)
            status, phone = get_phone_test(message_token)
            if status != '1':
                log_register.logger.error("手机号获取失败...")
                # print("手机号获取失败...")
                continue

            if auto_register_get_phone("86" + phone):
                log_register.logger.info("{}已经获取过".format(phone))
                continue

            log_register.logger.info(phone)

            # 尝试登录
            try_login(phone)
            time.sleep(5)

            # 拉取xml
            get_xml()
            # 判断结果
            code_tree = ET.parse("ui.xml")
            if if_node(code_tree, ".//node[@class='android.widget.EditText']", 0):
                # 若是已经注册过的号是给telegram端发验证码而不是手机
                if if_node(code_tree,
                           ".//node[@text=\"We've sent the code to the Telegram app on your other device.\"]", 0):
                    adb_tap(code_tree, ".//node[@text='Send the code as an SMS']", 0)
                    # auto_register_insert_phone("86" + phone, "registered")
                    # log_register.logger.info("已经注册过的")
                    # continue

                # 输入验证码
                input_code(phone)

                # 获取session
                save_session(phone)
                auto_register_insert_phone("86" + phone, "get session")
                end_time = time.time()
                log_register.logger.info("用时 {} s".format(end_time - start_time))

                from my_test.my_just_test2 import main_check
                main_check("86" + phone, end=end)

                # from myTelegram import MyTG
                # tg = MyTG()
                # tg.sign_in("86" + phone)
                # time.sleep(60)
                # tg.add_channel("my2020channela")
                # tg.send_message("my2020channela", "hello, {}".format("86" + phone))

                # print("#" * 10)
                # print(end_time - start_time)
                # print("#" * 10)
                # get_code_form_client()

                # 注销
                # logout()
            elif if_node(code_tree, ".//node[@text='Invalid phone number. Please check the number and try again.']", 0):
                log_register.logger.error("无效的手机号码")
                # print("无效的手机号码")
            else:
                pass

        except Exception as e:
            if e.__str__() == '{"error_code": 504, "msg": "获取验证码失败..."}':
                auto_register_insert_phone("86" + phone, "can not get code")
            log_register.logger.error(e)
            # print(e)
            # 手机号获取失败
            end_time = time.time()
            log_register.logger.info("用时 {} s".format(end_time - start_time))
            # end_time = time.time()
            # print("#" * 10)
            # print(end_time - start_time)
            # print("#" * 10)
            continue


if __name__ == '__main__':
    end = "85262999999"
    main(end)
