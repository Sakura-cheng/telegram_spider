import pymysql
from config import host, port, user, password, db


def get_db():
    try:
        return pymysql.connect(host=host, port=port, user=user, password=password, db=db)
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

    sql = "select * from user where user_id=%s"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()

    if user:
        print("该用户已存在...")
    else:
        sql = "insert into user (phone, user_id, first_name, last_name, username, bot) values (%s, %s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (phone, user_id, first_name, last_name, username, bot))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()


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


if __name__ == '__main__':
    print(get_phone())
