"""
房间管理
"""

from time import sleep


# 查找可用房间 -- FR1
def find_room(connfd, room_type, room_state, db):
    result = db.find_room(room_type, room_state)
    if result:
        print(result)
        connfd.send(str(result).encode())

        # for data in result:
        #     msg = "%s " % data
        #     connfd.send(msg.encode())
        #     sleep(0.1)
        # connfd.send(b"##")
    else:
        connfd.send(b'FAIL')


# 修改房间状态 --ARS1
def alter_room_state(connfd, room_number, room_state, db):
    if db.alter_room_state(room_number, room_state):
        connfd.send(b"ARS1OK")
    else:
        connfd.send(b"FAIL")


# 修改订单状态 -- AOS1
def alter_order_state(connfd, db, order_num, state, date, ulog):
    if db.alter_order_state(order_num, state, date, ulog):
        connfd.send(b"AOS1OK")
    else:
        connfd.send(b"FAIL")


# 查看预订记录 --SRR1
def show_reserve_record(connfd, reserve_date, reserve_state, db):
    result = db.show_reserve(reserve_date, reserve_state)
    if result:
        print(result)
        for data in result:
            msg = "%s|%s|%s|%s|%s|%s|%s|%s" % data
            connfd.send(msg.encode())
            sleep(0.1)
        connfd.send(b"##")
    else:
        connfd.send(b'FAIL')


# 生成预订订单 -- RR1
def reserve_room(connfd, db, rnum, arrival_datetime, departtuure_datetime,
                 retention_date, days, rtype, rprice, rquantity, guest_name,
                 guest_phone, rstate, rnotes, rnumber, rulog):
    print(rnum, arrival_datetime, departtuure_datetime,
          retention_date, days, rtype, rprice, rquantity, guest_name,
          guest_phone, rstate, rnotes, rnumber, rulog)
    if db.reserve_room(rnum, arrival_datetime, departtuure_datetime,
                       retention_date, days, rtype, rprice, rquantity,
                       guest_name, guest_phone, rstate, rnotes, rnumber, rulog):
        connfd.send(b"RR1OK")
    else:
        connfd.send(b'FAIL')


# 查看入住/退房列表 -- SCR1
def show_check_record(connfd, db, check_date, check_state, field_name):
    result = db.show_check(check_date, check_state, field_name)
    if result:
        print(result)
        for data in result:
            msg = "%s|%s|%s|%s|%s|%s|%s" % data
            connfd.send(msg.encode())
            sleep(0.1)
        connfd.send(b"##")
    else:
        connfd.send(b'FAIL')


# 生成入住订单 -- CIR1
def checkin_room(connfd, db, cnum, arrival_datetime,
                 departtuure_datetime, days, ctype,
                 cprice, c_rnumber, cnotes, cstate, culog):
    print(cnum, arrival_datetime,
          departtuure_datetime, days, ctype,
          cprice, c_rnumber, cnotes, cstate, culog)

    if db.checkin_record(cnum, arrival_datetime,
                         departtuure_datetime, days, ctype,
                         cprice, c_rnumber, cnotes, cstate, culog):

        connfd.send(b'CIR1OK')
    else:
        connfd.send(b'FAIL')


# 保存客人信息 -- CGR1
def save_ginfo(connfd, db, g_name, g_id_num, g_nationality,
               g_sex, g_site, g_phone, g_deposit, cnum):
    if db.save_guest_info(g_name, g_id_num, g_nationality,
                          g_sex, g_site, g_phone, g_deposit, cnum):
        connfd.send(b'CGR1OK')
    else:
        connfd.send(b'FAIL')


# 查询房间账单 --SRB1
def select_room_bill(connfd, db, rnumber, state):
    if db.select_bill(rnumber, state):
        cnum, date, ctype, cprice, gname, gdeposit = db.select_bill(rnumber, state)
        msg = '%s|%s|%s|%s|%s|%s' % (cnum, date, ctype, cprice, gname, gdeposit)
        print(msg)
        connfd.send(msg.encode())
    else:
        connfd.send(b"FAIL")


# 　退房结账
def checkout_room(connfd, db, rnumber, state):
    result = db.checkout_record(rnumber, state)
    if result:
        pass


# 查看房态
def show_room_dynamic(connfd, db):
    resutl = db.show_room_dynamic()
    if resutl:
        connfd.send(str(resutl).encode())
    else:
        connfd.send(b"FAIL")


# 查看房情
def show_room_availability(connfd, db, datetime):
    # 所有房型及房量
    result1 = db.select_room_quantity()
    # 预订所占房型及房量
    result2 = db.select_reserve_number(datetime)
    # 入住所占房型及房量
    result3 = db.select_not_checkout_number(datetime)
    msg = "%s|%s|%s" % (result1, result2, result3)
    print(msg)
    connfd.send(msg.encode())
