"""
房间管理
"""

from datetime import datetime
from itertools import chain
from decimal import Decimal,ROUND_HALF_UP
from collections import Counter
import random

# 酒店编号
HOTEL_NUMBER = '0737'
# 房型房态
RSTATE = {1: '干净房', 2: '预订房', 3: '入住房', 4: '脏房', 5: '维修房'}
RTYPE = {1: '单人间', 2: '标准间', 3: '商务间', 4: '豪华间'}


# 生成当前时间
def maker_datetime():
    # 将datetime格式化去掉毫秒
    now_time = datetime.now().replace(microsecond=0)
    return now_time


# 金额格式化(四舍五入,保留两位小数)
def number_round(value):
    # 将传入的字符串数据(类数字)进行是四舍五入计算,并保留两位小数点
    return Decimal(value).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


# 日期转换函数
def parse_ymd(date, h):
    year_s, mon_s, day_s = date.split(',')
    return datetime(int(year_s), int(mon_s), int(day_s), int(h))


# 生成预订单号
def rid_maker(hotel_number):
    date = '{0:%y%m%d%M%S}'.format(datetime.now())
    randomnum = random.randint(0, 99)
    if randomnum < 10:
        randomnum = str(0) + str(randomnum)
    rid = date + str(hotel_number) + str(randomnum)
    return rid


# 生成入住单号
def io_id_maker(hoter_number):
    date = '{0:%y%m%d}'.format(datetime.now())
    randomnum = random.randint(0, 999)
    if randomnum < 10:
        randomnum = str(00) + str(randomnum)
    elif randomnum < 100:
        randomnum = str(0) + str(randomnum)
    io_id = str(date) + str(hoter_number) + str(randomnum)
    return io_id


# 修改房间数量(暂未上线)
# def alter_room_quantity(sock, rtype, rquantity):
#     msg = "ARQ1|%s|%s" % (rtype, rquantity)
#     sock.send(msg.encode())
#     result = sock.recv(1024).decode()
#     if result[0] == 'ARQ1OK':
#         return True
#     else:
#         return False

# 修改房间状态 --ARS1
def alter_room_state(sock, state, room_number):
    # 改变房间状态
    msg = 'ARS1|%s|%s' % (room_number, state)
    sock.send(msg.encode())
    result = sock.recv(1024).decode()
    print(result)
    if result == 'ARS1OK':

        # print('修改成功')
        return True
    else:
        # print('修改失败！')
        return False


# 查找可用房 -- FR1
def find_room(sock, rtype, state_1, state_2):
    # 查询房间
    msg = 'FR1|%s|%s' % (rtype, state_1)
    sock.send(msg.encode())
    data = sock.recv(1024 * 100).decode()
    if data != 'FAIL':

        result = eval(data)
        # 将二维元组组合为一维元组,并转换为列表
        rnumber_list = list(chain.from_iterable(result))

        i = 0
        while i < len(rnumber_list):
            print('可用房间号为：', rnumber_list)
            rnumber = int(input('请选择房间号：'))
            if rnumber not in rnumber_list:
                print("输入错误，请重新输入")
                continue
            else:
                # # 修改房间状态为已预定
                # rstate = 2
                result = alter_room_state(sock, state_2, rnumber)
                if result:
                    print('排房成功')
                    return rnumber
                else:
                    i += 1
                    continue
        else:
            print("暂无可用房间，请稍后选择")
            return False
    else:
        print('暂无可用房')
        return False


# 修改订单状态 -- AOS1
def alter_order_state(sock, state, order_num, date, ulog):
    msg = "AOS1|%s|%s|%s|%s" % (order_num, state, date, ulog)
    sock.send(msg.encode())
    result = sock.recv(128).decode()
    if result == "AOS1OK":
        return True
    else:
        return False


# 　选择房型房价(为省事,我把房型房价写死了...后续再进行优化)
def choose_room_type_price():
    # sock.send(b"CRTP1")
    # data = sock.recv(1024 * 10).decode()
    # result = eval(data)

    price = 0
    while True:
        print("""
                ╔=====  房型  =======╗

                    1.单人间 699.00
                    2.标准间 799.00
                    3.商务间 899.00
                    4.豪华间 999.00           

                ╚====================╝
                """)
        rtype = input("请选择房型（1，2，3，4）：")
        if rtype == '1':
            price = 699.00
            break
        elif rtype == '2':
            price = 799.00
            break
        elif rtype == '3':
            price = 899.00
            break
        elif rtype == '4':
            price = 999.00
            break
        else:
            print('输入错误，请重新输入')
            continue
    return rtype, price


# 查看预订列表 --SRR1
def show_reserve_record(sock):
    re_date = input("请输入日期（年，月，日）：")
    try:
        re_date = parse_ymd(re_date, 12)
    except:
        print("日期错误！")
        return

    re_state = input('请输入订单状态（1.有效 2.取消 3.过期）：')
    if re_state not in ['1', '2', '3']:
        print('无该状态订单！')
        return
    msg = "SRR1|%s|%s" % (re_date, re_state)
    sock.send(msg.encode())
    print("""
            +--------------+--------+--------+--------+--------+---------------+--------------------------+-----------------------+
            |    预订号     |   姓名  |  房类   |  房数   |  房价  |    联系方式     |        到店日期           |        离店日期         |
            +--------------+--------+--------+--------+--------+---------------+--------------------------+-----------------------+
    """)
    while True:
        data = sock.recv(1024).decode()
        if data == 'FAIL':
            print("""                        
            |                                                  当前时间没有预订！                                                        |
                        
                """)
            break
        else:
            result = data.split('|')
            if data == "##":
                break
            print("""
            |  %s  |  %s  |   %s    |   %s   | %s  |   %s  |   %s   |  %s  |
            |                                                              |
            +-----------------------------------------------------------------------------------------------------------------------+
                """ % (result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))


# 预定房间 --  RR1
def reserve_room(sock, user_name):
    arrival_date = input('请输入到店日期（年，月，日）：')
    departtuure_date = input('请输入离店日期（年，月，日）：')
    try:
        # 格式化日期时间
        arrival_datetime = parse_ymd(arrival_date, 12)
        departtuure_datetime = parse_ymd(departtuure_date, 12)
        # 保留时间
        retention_date = parse_ymd(arrival_date, 18)
        days = (departtuure_datetime - arrival_datetime).days
    except:
        print("日期输入错误")
        return

    # 获取房间类型及房价
    rtype, rprice = choose_room_type_price()
    rquantity = int(input("请输入预订数量："))

    guest_name = input("请输入客人姓名：")
    guest_phone = input("请输入客人手机号：")

    # 暂时只能给一间房排房
    if rquantity > 1:
        rnumber = 0
    else:
        choose = input("是否预订房间号（Y:是，N：否）：")
        if choose == "Y":
            # 干净房
            state_1 = 1
            # 已预订
            state_2 = 2
            result = find_room(sock, rtype, state_1, state_2)
            if result:
                rnumber = result
            else:
                rnumber = 0





        else:
            rnumber = 0

    choose = input('是否输入备注（Y:是，N：否）：')
    if choose == "Y":
        rnotes = input('请输入备注信息；')
    else:
        rnotes = ' '

    # 订单状态初始为1(有效)
    rstate = 1
    # 编写操作日志
    rulog = '%s 操作 预订' % user_name

    # 生成预订单号
    rnum = rid_maker(HOTEL_NUMBER)

    msg = 'RR1|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' \
          % (rnum, arrival_datetime, departtuure_datetime, retention_date, days,
             rtype, rprice, rquantity, guest_name, guest_phone, rstate, rnotes, rnumber, rulog)
    sock.send(msg.encode())
    result = sock.recv(1024).decode()
    if result == "RR1OK":
        print('预订成功')
    else:
        print('网络错误，预订失败')
    return


# 查询入住/退房订单 -- SCR1
def show_record(sock, state):
    ce = input("请输入日期（年，月，日）：")
    try:
        year_s, mon_s, day_s = ce.split(',')
        ce_date = datetime(int(year_s), int(mon_s), int(day_s)).date()
    except:
        print("日期错误！")
        return

    # 订单状态
    ce_state = state
    field_name = ''
    if ce_state == 1:
        field_name = 'c_arrival_date'
    if ce_state == 0:
        field_name = 'c_departture_date'
    msg = "SCR1|%s|%s|%s" % (ce_date, ce_state, field_name)
    print(msg)
    sock.send(msg.encode())
    print("""
                    +--------------+--------+--------+--------+---------------+--------------------------+------------------------+
                    |    订单号     |   姓名  |  房类   |   房价  |    联系方式     |        到店日期           |        离店日期         |
                    +--------------+--------+---------+--------+---------------+--------------------------+-----------------------+
            """)
    while True:
        data = sock.recv(1024).decode()
        if data == 'FAIL':
            print("""                        
                    |                                                  当前时间没有记录！                                              |

                        """)
            break
        else:
            result = data.split('|')
            if data == "##":
                break
            print("""
                    |  %s  |  %s  |   %s    |   %s   | %s  |   %s  |   %s   |
                    |                                                              
                    +-----------------------------------------------------------------------------------------------------------------------+
                        """ % (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))


# 查看入住列表 SCR1
def show_checkin_record(sock):
    # 1:在住
    show_record(sock, 1)


# 入住房间 -- CIR1 --CGR1
def checkin_room(sock, user_name):
    # 生成当前时间为入住时间
    arrival_datetime = maker_datetime()
    departtuure_date = input('请输入离店日期（年，月，日）：')
    try:
        # 格式化为离店日期时间
        departtuure_datetime = parse_ymd(departtuure_date, 12)

        # 计算入住时间与离店时间相差的天数
        beg_date = arrival_datetime.date()
        end_date = departtuure_datetime.date()
        days = (end_date - beg_date).days
    except:
        print("日期输入错误")
        return

    # 获取房间类型及房价
    ctype, cprice = choose_room_type_price()

    # 选择房间号并改变其状态(1. 干净房)
    state_1 = 1
    # 已入住
    state_2 = 3
    result = find_room(sock, ctype, state_1, state_2)
    if result:
        c_rnumber = result
    else:
        print('无法入住')
        return

    choose = input('是否输入备注（Y:是，N：否）：')
    if choose == "Y":
        cnotes = input('请输入备注信息；')
    else:
        cnotes = ' '
    # 订单状态初始为1(在住)
    cstate = 1
    # 编写操作日志
    culog = '%s 操作 入住' % user_name

    # 生成订单号
    cnum = io_id_maker(HOTEL_NUMBER)

    # 编写请求
    c_msg = 'CIR1|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (cnum, arrival_datetime,
                                                    departtuure_datetime, days,
                                                    ctype, cprice, c_rnumber, cnotes, cstate, culog)

    sock.send(c_msg.encode())
    result = sock.recv(128).decode()
    # print(result)
    if result == 'CIR1OK':
        print('操作成功')
        g_name = input("请输入客人姓名：")
        g_id_num = input('请输入客人证件号：')
        g_nationality = input('请输入客人国籍：')
        g_sex = input('请输入客人性别（1.男，2.女）：')
        g_site = input('请输入客人地址：')
        g_phone = input("请输入客人手机号：")
        g_deposit = input('请录入客人押金：')
        # 发送请求，保存客人信息
        g_msg = 'CGR1|%s|%s|%s|%s|%s|%s|%s|%s' % (g_name, g_id_num, g_nationality,
                                                  g_sex, g_site, g_phone, g_deposit, cnum)
        sock.send(g_msg.encode())
        result = sock.recv(1024).decode()
        if result == 'CGR1OK':
            print('入住成功')
        else:
            print('网络波动，入住失败')
        return

    else:
        print('操作失败，请检查后再办理入住')
        return


# 查看退房列表 --SCR0
def show_checkout_record(sock):
    # 0: 退房
    show_record(sock, 0)


# 　退房结账 -- SRB1
def checkout_room(sock, user_name):
    co_rnumber = input('请输入退房房间号：')
    # 查询账单
    # 订单状态为 1（在住）
    state = 1
    msg = 'SRB1|%s|%s' % (co_rnumber, state)
    sock.send(msg.encode())
    data = sock.recv(1024 * 10).decode()
    if data != 'FAIL':
        # print(data)
        result = data.split('|')
        print(result)

        # 生成退房日期
        departture_date = maker_datetime()

        # 订单号
        cnum = result[0]
        # 到店日期
        arrival_date = result[1]

        # 暂时把房型写死
        co_type = result[2]
        rtype = ''
        if co_type == '1':
            rtype = '单人间'
        if co_type == '2':
            rtype = '标准间'
        if co_type == '3':
            rtype = '商务间'
        if co_type == '4':
            rtype = '豪华间'
        # 房价格式化输出保留两位小数
        cprice = number_round(result[3])
        # print(type(cprice))
        # 客人姓名
        guest_name = result[4]
        # 客人押金格式化输出保留两位小数
        guest_deposit = number_round(result[5])
        # print(type(guest_deposit))

        # 计算入住天数
        begin_date = departture_date.date()

        end_date = datetime.strptime(arrival_date, '%Y-%m-%d %H:%M:%S').date()

        cdays = (begin_date - end_date).days

        # 计算消费金额
        total_money = cdays * cprice
        # print(total_money)
        # print(type(total_money))

        # 计算余额
        surplus_money = guest_deposit - total_money

        # 打印账单
        print("""
                ╔================  账单  =================╗
                      
                      宾客姓名：     %s
                      到店日期：     %s
                      离店日期：     %s
                      房型：        %s
                      房价：        %s
                      房号：        %s           
                      消费：        %s
                      预付：        %s
                      余额：        %s
                                          
                ╚=========================操作人：%s======╝
        """ % (guest_name, arrival_date, departture_date, rtype, cprice,
               co_rnumber, total_money, guest_deposit, surplus_money, user_name))

        # 修改订单状态为退房,并更新退房时间额和操作日志
        i = 0
        while i < 5:
            state = 0
            ulog = '%s 操作 退房\n' % user_name
            if alter_order_state(sock, state, cnum, departture_date, ulog):
                # 修改房间状态为脏房
                rstate = 4
                if alter_room_state(sock, rstate, co_rnumber):
                    print('退房成功')
                    return
                else:
                    i += 1
                    continue
            else:
                i += 1
                continue
        else:
            print('退房失败，请刷新。')
            return


    else:
        print('未查到该房间有入住记录')
        return


# 修改房态
def alter_rstate(sock):
    rnumber = input('请输入房间号：')
    rstate = input("修改为（1.干净房，4.脏房，5.维修房）：")
    if rstate not in ('1', '4', '5'):
        print('输入错误')
        return
    if alter_room_state(sock, rstate, rnumber):
        print('修改成功')
    else:
        print('修改失败，请稍后再试')
    return


# 查看房态 -- SRD1
def show_room_dynamic(sock, user_name):
    sock.send(b'SRD1')
    result = sock.recv(1024 * 100).decode()
    if result != 'FAIL':
        room_list = eval(result)
        # print(room_list)
        # print(type(room_list)
        print("""
                        ╔================  房态  =================╗
            """)
        for i in room_list:
            rtype = i[2].split(',')

            # print(rstate[i[0]],i[1],i[2])
            print("""
                                %s:  %s  
                                房型：  %s                              
                        """ % (RSTATE[i[0]], i[1], rtype))

        print("""
                        ╚=========================操作人：%s======╝
            """ % user_name)


# 查看房情 -- SRA1
def show_room_availability(sock, user_name):
    date = input('请输入查询日期(年,月,日)：')
    try:
        # 生成当天日期
        datetime = parse_ymd(date, 12)
    except:
        print('日期错误！')
        return

    msg = 'SRA1|%s' % datetime
    sock.send(msg.encode())
    result = sock.recv(1024 * 100).decode().split('|')
    print(result)
    # 所有房型及房量
    total = Counter(dict(eval(result[0])))
    print(total)
    # 预订所占房型及房量
    reserve = Counter('0')
    # 入住所占房型及房量
    checkin = Counter('0')
    if result[1] != '0':
        reserve = Counter(dict(eval(result[1])))
    if result[2] != '0':
        checkin = Counter(dict(eval(result[2])))

    # 计算可用房型及房量
    usable = total - (reserve + checkin)

    print('total:', total)
    print('reserve:', reserve)
    print('checkin:', checkin)

    print("""
                ╔================  房情  =================╗
                                    %s
                        房型      总房量     可用房
            """ % datetime.date())

    for k in total:
        print("""                       %s        %s        %s""" % (RTYPE[k], total[k], usable[k]))

    print("""
                ╚=========================操作人：%s======╝
    """ % user_name)
