import requests
from config import message_name, message_sid, message_password, message_api_name, message_token
import time
import re
import socket
socket.setdefaulttimeout(30)

url = "http://api.banma1024.net/api/do.php"


def login():
    '''
    登录斑马获取token
    :return:
    '''
    params = {
        "action": "loginIn",
        "name": message_api_name,
        "password": message_password
    }
    response = requests.get(url, params=params).text
    print(response)
    result = response.split("|")
    return result[0], result[1]


def get_phone(token, phone):
    params = {
        "action": "getPhone",
        "sid": message_sid,
        "token": token,
        "phone": phone
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    return result[0], result[1]


def get_phone_test(token):
    params = {
        "action": "getPhone",
        "sid": message_sid,
        "token": token
    }
    response = requests.get(url, params=params).text
    print(response)
    result = response.split("|")

    return result[0], result[1]


def get_message(token, phone):
    params = {
        "action": "getMessage",
        "sid": message_sid,
        "phone": phone,
        "token": token,
        "author": message_name
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    print(result)
    return result[0], result[1]


def cancel_recv(token, phone):
    params = {
        "action": "cancelRecv",
        "sid": message_sid,
        "phone": phone,
        "token": token
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    return result[0], result[1]


def cancel_all_recv(token):
    params = {
        "action": "cancelAllRecv",
        "token": token
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    print('释放手机号')
    return result[0], result[1]


def add_black(token, phone):
    params = {
        "action": "addBlacklist",
        "sid": message_sid,
        "phone": phone,
        "token": token
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    print("加入黑名单: " + result[1])
    return result[0], result[1]


def get_summary(token):
    params = {
        "action": "getSummary",
        "token": token
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    print(result)
    return result[0], result[1]


def get_code(phone):
    '''
    获取对应手机号的验证码
    :param phone:
    :return:
    '''
    # try:
    #    login_status, token = login()
    # except Exception as e:
    #    print(e)
    #   raise RuntimeError('{"error_code": 505, "msg": "斑马api登录失败..."}')
    # phone_status, phone_ = get_phone(message_token, phone)

    # if phone_status == '0':
    #     raise RuntimeError('{"error_code": 503, "msg": "无法获取该手机号..."}')
    # else:
    #     print(phone_)
    print('等待获取' + phone + '收到的验证码')
    message_status, message = get_message(message_token, phone)

    try_num = 20
    while message_status == '0' and try_num > 0:
        # print(message)
        time.sleep(5)
        message_status, message = get_message(message_token, phone)
        try_num -= 1

    if try_num <= 0:
        # 加入黑名单
        # add_black(message_token, phone)
        cancel_all_recv(message_token)
        raise RuntimeError('{"error_code": 504, "msg": "获取验证码失败..."}')

    print("message: " + message)
    code = re.search('\d\d\d\d\d', message).group()
    # if message.startswith("【CMK】"):
    #     code = message.split("】")[1]
    # elif message.startswith("[MTTO]"):
    #     code = message.split(": ")[1]
    # else:
    #     code = message.split(": ")[1]

    print("code: " + code)
    return code


if __name__ == '__main__':
    login()
    # cancel_all_recv(message_token)
    # status, phone = get_phone_test(message_token)
    # input('开始接受验证码了吗？')
    # time.sleep(10)
    # code = get_code(phone)
    # print(code)
