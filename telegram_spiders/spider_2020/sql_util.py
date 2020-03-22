import pymysql
from config import host, port, user, password, db, sessions_dir
import datetime
import os


def get_db():
    try:
        # return pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        return pymysql.connect(host=host, port=port, user=user, password=password, db=db, use_unicode=True,
                               charset="utf8")
    except Exception as e:
        print("数据库连接失败")
        print(e)


def get_phone(category):
    '''
    获取手机号
    :return:
    '''
    conn = get_db()
    sql = "select phone, id from phone where status=-1 and category=%s limit 1"
    cursor = conn.cursor()
    cursor.execute(sql, (category,))
    result = cursor.fetchone()
    if result is not None:
        phone = result[0]
        id = result[1]
    else:
        phone = None
        id = None
    conn.close()
    return phone, id


def change_status(phone_id, status):
    '''
    获取所有信息后修改状态
    :param phone:
    :return:
    '''
    conn = get_db()
    cursor = conn.cursor()

    sql = "update phone set status=%s where id = %s"
    try:
        cursor.execute(sql, (status, phone_id))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    conn.close()


def insert_user_info(user_info):
    phone = user_info["phone"]
    user_id = user_info["id"]
    first_name = user_info["first_name"]
    last_name = user_info["last_name"]
    username = user_info["username"]
    bot = 1 if user_info["bot"] else 0

    conn = get_db()
    cursor = conn.cursor()

    # sql = "select * from user where user_id=%s"
    # cursor.execute(sql, (user_id,))
    # user = cursor.fetchone()

    # if user:
    #     print("该用户已存在...")
    # else:

    # sql = "insert ignore into user (phone, user_id, first_name, last_name, username, bot) values (%s, %s,%s,%s,%s,%s)"
    if phone is not None:
        sql = "insert into user (phone, user_id, first_name, last_name, username, bot) values (%s,%s,%s,%s,%s,%s) on duplicate key update phone=values(phone)"
    else:
        sql = "insert ignore into user (phone, user_id, first_name, last_name, username, bot) values (%s,%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (phone, user_id, first_name, last_name, username, bot))
        conn.commit()
        print(str(user_id) + '插入user信息成功')
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


def insert_many_user_info(user_info_list):
    data = []
    for user_info in user_info_list:
        phone = user_info["phone"]
        user_id = user_info["id"]
        first_name = user_info["first_name"]
        last_name = user_info["last_name"]
        username = user_info["username"]
        bot = 1 if user_info["bot"] else 0
        tup = (phone, user_id, first_name, last_name, username, bot)
        data.append(tup)

    conn = get_db()
    cursor = conn.cursor()

    # sql = "select * from user where user_id=%s"
    # cursor.execute(sql, (user_id,))
    # user = cursor.fetchone()

    # if user:
    #     print("该用户已存在...")
    # else:

    sql = "insert ignore into user (phone, user_id, first_name, last_name, username, bot) values (%s, %s,%s,%s,%s,%s)"
    try:
        cursor.executemany(sql, data)
        conn.commit()
        print('插入user信息成功')
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


def insert_check_user_info(user_info, phone, by_phone):
    phone = phone
    user_id = user_info["id"]
    first_name = user_info["first_name"]
    last_name = user_info["last_name"]
    username = user_info["username"]
    bot = 1 if user_info["bot"] else 0
    status = None
    if user_info["status"]:
        if user_info["status"]["was_online"]:
            status = user_info["status"]["was_online"]
        elif user_info["status"]["expires"]:
            status = user_info["status"]["expires"]

    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from check_user where phone=%s"
    cursor.execute(sql, (phone,))
    user = cursor.fetchone()

    if user:
        print("该手机号已存在...")
    else:
        sql = "insert into check_user (phone, user_id, first_name, last_name, username, status, bot, by_phone, by_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (
                phone, user_id, first_name, last_name, username, status, bot, by_phone, datetime.datetime.now()))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def selcet_the_last_check_user(start):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from check_user order by phone desc limit 1"
    cursor.execute(sql)
    user = cursor.fetchone()
    if user:
        return user[1]
    else:
        return None


def get_the_count_of_check_user():
    conn = get_db()
    cursor = conn.cursor()

    sql = "select count(phone) from check_user"
    cursor.execute(sql)
    count = cursor.fetchone()
    return count[0]


def get_the_phone_from_check_user_by_index(index):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select phone from check_user limit %s, 1"
    cursor.execute(sql, (index,))
    phone = cursor.fetchone()
    return phone[0]


def get_info_from_check_user_by_phone(phone):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from check_user where phone=%s"
    cursor.execute(sql, (phone,))
    info = cursor.fetchone()
    return info


def insert_authorization(authorization_info, user_id):
    hash = str(authorization_info["hash"])
    device_model = authorization_info["device_model"]
    platform = authorization_info["platform"]
    system_version = authorization_info["system_version"]
    app_name = authorization_info["app_name"]
    app_version = authorization_info["app_version"]
    date_created = authorization_info["date_created"]
    date_active = authorization_info["date_active"]
    ip = authorization_info["ip"]
    country = authorization_info["country"]
    region = authorization_info["region"]
    official_app = 1 if authorization_info["official_app"] else 0

    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from authorization where hash=%s"
    cursor.execute(sql, (hash,))
    authorization = cursor.fetchone()

    if authorization and hash != '0':
        print("该authorization已存在...")
    elif authorization and hash == '0':
        print("更新该authorization...")
        sql = "update authorization set user_id=%s, hash=%s, device_model=%s, platform=%s, system_version=%s, " \
              "app_name=%s, app_version=%s, date_created=str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%s'), " \
              "date_active=str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%s'), ip=%s, country=%s, region=%s, official_app=%s " \
              "where hash='0' "
        try:
            cursor.execute(sql, (
                user_id, hash, device_model, platform, system_version, app_name, app_version, date_created, date_active,
                ip, country, region, official_app))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    else:
        sql = "insert into authorization (user_id, hash, device_model, platform, system_version, app_name, " \
              "app_version, date_created, date_active, ip, country, region, official_app) values (%s, %s, %s, %s, %s, " \
              "%s, %s, str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%s'), str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%s'), %s, %s, " \
              "%s, %s) "

        try:
            cursor.execute(sql, (
                user_id, hash, device_model, platform, system_version, app_name, app_version, date_created, date_active,
                ip, country, region, official_app))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_message(message_info, user_id):
    message_id = message_info["id"]
    message = message_info["message"]
    date = message_info["date"]
    from_id = message_info["from_id"]
    to_id = message_info["to_id"]

    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from message where message_id=%s and from_id=%s and to_id=%s"
    cursor.execute(sql, (message_id, from_id, to_id))
    m = cursor.fetchone()

    if m:
        print("该message已存在...")
    else:
        sql = "insert into message (user_id, message_id, message, date, from_id, to_id) values (%s, %s, %s, str_to_date(%s," \
              "'%%Y-%%m-%%d %%H:%%i:%%s'), %s, %s) "
        try:
            cursor.execute(sql, (user_id, message_id, message, date, from_id, to_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_contact(user_id, contact_user_id):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from contact where user_id=%s and contact_user_id=%s"
    cursor.execute(sql, (user_id, contact_user_id))
    relationship = cursor.fetchone()

    if relationship:
        print("该contact已存在...")
    else:
        try:
            sql = "insert into contact (user_id, contact_user_id) values (%s, %s)"
            cursor.execute(sql, (user_id, contact_user_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_channel(channel_info, user_id, num):
    channel_id = channel_info["id"]
    title = channel_info["title"]
    username = channel_info["username"]

    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from channel where channel_id=%s"
    cursor.execute(sql, (channel_id,))
    channel = cursor.fetchone()

    if channel:
        print("该channel已存在...")
    else:
        try:
            sql = "insert into channel (user_id, channel_id, title, username, participants_count) values (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_id, channel_id, title, username, num))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_channel_user(channel_id, user_id):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from channel_user where channel_id=%s and user_id=%s"
    cursor.execute(sql, (channel_id, user_id))
    relationship = cursor.fetchone()

    if relationship:
        print("该channel_user已存在...")
    else:
        try:
            sql = "insert into channel_user (channel_id, user_id) values (%s, %s)"
            cursor.execute(sql, (channel_id, user_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_channel_many_user(channel_id, user_list):
    conn = get_db()
    cursor = conn.cursor()

    data = []
    for user in user_list:
        tup = (channel_id, user["id"])
        data.append(tup)

    try:
        sql = "insert ignore into channel_user (channel_id, user_id) values (%s, %s)"
        cursor.executemany(sql, data)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


def insert_group(group_info, user_id, num):
    group_id = group_info["id"]
    title = group_info["title"]

    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from group_ where group_id=%s"
    cursor.execute(sql, (group_id,))
    group = cursor.fetchone()

    if group:
        print("该group已存在...")
    else:
        try:
            sql = "insert into group_ (user_id, group_id, title, participants_count) values (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, group_id, title, num))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_group_user(group_id, user_id):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from group_user where group_id=%s and user_id=%s"
    cursor.execute(sql, (group_id, user_id))
    relationship = cursor.fetchone()

    if relationship:
        print("该channel_user已存在...")
    else:
        try:
            sql = "insert into group_user (group_id, user_id) values (%s, %s)"
            cursor.execute(sql, (group_id, user_id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


def insert_group_many_user(group_id, user_list):
    conn = get_db()
    cursor = conn.cursor()

    data = []
    for user in user_list:
        tup = (group_id, user["id"])
        data.append(tup)

    try:
        sql = "insert ignore into group_user (group_id, user_id) values (%s, %s)"
        cursor.executemany(sql, data)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


def insert_phone(phone, origin_ip, destination_ip):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from phone where phone = %s"
    cursor.execute(sql, (phone))
    phone_existed = cursor.fetchone()

    if phone_existed:
        print('该手机号已经在数据库中...')
    else:
        try:
            sql = "insert into phone (phone, origin_ip, destination_ip) values (%s, %s, %s)"
            cursor.execute(sql, (phone, origin_ip, destination_ip))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


def insert_session(phone, session):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from login_phone where phone = %s and session is not null"
    cursor.execute(sql, (phone))
    phone_existed = cursor.fetchone()

    if phone_existed:
        print('该手机号已经在数据库中...')
    else:
        try:
            sql = "insert into login_phone (phone, session, time) values (%s, %s, %s)"
            cursor.execute(sql, (phone, session, datetime.datetime(2019, 1, 1)))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


def insert_session_platform(phone, session):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select * from platform_login_phone where phone = %s and session is not null"
    cursor.execute(sql, (phone))
    phone_existed = cursor.fetchone()

    if phone_existed:
        print('该手机号已经在数据库中...')
    else:
        try:
            sql = "insert into platform_login_phone (phone, session, time) values (%s, %s, %s)"
            cursor.execute(sql, (phone, session, datetime.datetime.now()))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


def update_session_time(phone, use_time):
    conn = get_db()
    cursor = conn.cursor()

    try:
        sql = "update login_phone set time=%s where phone=%s"
        cursor.execute(sql, (use_time, phone))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def delete_session(phone):
    conn = get_db()
    cursor = conn.cursor()

    try:
        sql = "update login_phone set session=NULL where phone=%s"
        cursor.execute(sql, (phone))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def get_session(phone):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select session, time from login_phone where phone=%s"
    cursor.execute(sql, (phone))
    result = cursor.fetchone()
    if result is not None:
        session = result[0]
        time = result[1]
    else:
        session = None
        time = None
    conn.close()
    return session, time


def get_session_platform(phone):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select session, time from platform_login_phone where phone=%s"
    cursor.execute(sql, (phone))
    result = cursor.fetchone()
    if result is not None:
        session = result[0]
        time = result[1]
    else:
        session = None
        time = None
    conn.close()
    return session, time


def get_login_phones():
    conn = get_db()
    cursor = conn.cursor()

    sql = "select phone from login_phone where session is not null"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    return result


# 自动注册所需要的，避免重复从接码平台获取同一个手机号
def auto_register_get_phone(phone):
    conn = get_db()
    cursor = conn.cursor()

    sql = "select phone from check_phones where phone=%s"
    cursor.execute(sql, (phone))
    result = cursor.fetchone()
    if result is not None:
        conn.close()
        return True
    else:
        conn.close()
        return False


def auto_register_insert_phone(phone, category):
    conn = get_db()
    cursor = conn.cursor()

    sql = "insert ignore into check_phones (phone, category, time) values (%s, %s, %s)"
    try:
        cursor.execute(sql, (phone, category, datetime.datetime.now()))
        conn.commit()
        print('插入phone信息成功')
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


if __name__ == '__main__':
    count = get_the_count_of_check_user()
    print(count)
    import random

    index = random.randint(0, count - 1)
    phone = get_the_phone_from_check_user_by_index(0)
    print(phone)

    info = get_info_from_check_user_by_phone("85262008167")
    print(info)
    # auto_register_insert_phone("my_test", "my_test")
    # participants = []
    #
    # import time
    #
    # start_time = time.time()
    # iid = 1234567890
    # for i in range(100):
    #     iid += i
    #     participantest = {
    #         "phone": "",
    #         "id": iid,
    #         "first_name": None,
    #         "last_name": None,
    #         "username": None,
    #         "bot": False
    #     }
    #     participants.append(participantest)
    # insert_many_user_info(participants)
    # insert_channel_many_user(1472612002, participants)
    # print(time.time() - start_time)

    # insert_session_platform('1', '1')

    # import datetime
    #
    # update_session_time('12', datetime.datetime.now())
    # get_session('8615201615409')
    # print(datetime.datetime.now() - datetime.datetime(2018, 12, 1) > datetime.timedelta(seconds=3600))
    # get_login_phones()
    # fs = os.listdir(sessions_dir)
    # for f in fs:
    #     # print(f.split('_')[0])
    #     phone = f.split('_')[0]
    #     with open(sessions_dir + f, 'r') as ff:
    #         session = ff.read()
    #     print(phone, session)
    #     insert_session(phone, session)
