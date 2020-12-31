"""


"""

import pymysql
import hashlib

# 连接数据库的字典
DATABASE = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "951101",
    "database": "Hotel",
    "charset": "utf8"
}


# 密码加密
def change_passwd(passwd):
    hash = hashlib.md5()  # 加密算法对象
    hash.update(passwd.encode())  # 加密处理
    return hash.hexdigest()  # 获取加密后的结果


class Database:
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(**DATABASE)

    def create_cursor(self):
        """
        创建游标
        :return:
        """
        self.cur = self.db.cursor()

    def close(self):
        self.db.close()

    # ------------------------------------------------- User -----------------------------------------------------------

    # 登录
    def login(self, uphone, passwd):
        passwd = change_passwd(passwd)

        sql = "select position,user_name from users " \
              "where user_phone= %s and password = %s limit 1;"
        self.cur.execute(sql, [uphone, passwd])
        result = self.cur.fetchone()
        print('0000')
        if result:
            return result
        else:
            return False

    # 处理用户查询 -- F1
    def find_user(self, uname, uphone):
        sql = "select uid,user_name,user_phone,position" \
              " from users where user_name = %s and user_phone = %s limit 1; "
        self.cur.execute(sql, [uname, uphone])
        result = self.cur.fetchone()
        print('1111')
        if result:
            return result
        else:
            return False

    # 处理用户添加 -- A1
    def add_user(self, uname, uphone, passwd, position):
        sql = "select user_name from users where user_phone = %s limit 1;"
        self.cur.execute(sql, [uphone, ])
        print('2222')
        # 如果查询到该用户存在
        if self.cur.fetchone():
            return False

        # 插入用户,密码加密
        passwd = change_passwd(passwd)
        sql = "insert into users (user_name,user_phone,password,position) values (%s, %s, %s, %s);"
        try:
            self.cur.execute(sql, [uname, uphone, passwd, position, ])
            print('3333')
            self.db.commit()
            return True
        # 插入失败,回滚操作
        except:
            self.db.rollback()
            return False

    # 处理用户删除 -- D1
    def del_user(self, uid):
        sql = "delete from users where uid = %s limit 1;"
        try:
            self.cur.execute(sql, [uid, ])
            print('4444')
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 处理用户修改 -- U1
    def update_user(self, field_name, info, uid):
        sql = "update users set %s = '%s' where uid = %s limit 1;" % (field_name, info, uid)
        try:
            self.cur.execute(sql)
            print('5555')
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 处理用户密码修改
    def update_passwd(self, info, uid):
        new_passwd = change_passwd(info)
        sql = "update users set password = %s where uid = %s limit 1;"
        try:
            self.cur.execute(sql, [new_passwd, uid, ])
            print('6666')
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 处理显示所有用户 -- S1
    def show_user(self):
        sql = "select uid, user_name, user_phone, position from users;"
        self.cur.execute(sql)
        print('7777')
        return self.cur.fetchall()

    # ----------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------ Room ----------------------------------------------------------------

    # 查找可用房间  -- FR1
    def find_room(self, room_type, room_state):
        sql = 'select room_number from room_info where r_sid = %s and r_tid = %s;'
        self.cur.execute(sql, [room_state, room_type, ])
        print('9999')
        result = self.cur.fetchall()
        print(result)
        if result:
            return result
        else:
            return False

    # 修改房间状态 --ARS1
    def alter_room_state(self, rnumber, rstate):
        sql = 'update room_info set r_sid = %s where room_number = %s;'
        try:
            self.cur.execute(sql, [rstate, rnumber])
            print("1010")
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 修改订单状态 -- AOS1
    def alter_order_state(self, onum, state, date, ulog):
        sql = 'update io_record set c_state = %s,c_departture_date = %s,c_ulog = concat(%s,c_ulog) where c_order_number = %s;'
        try:
            self.cur.execute(sql, [state, date, ulog, onum])
            print('1818')
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 查看预订记录 --SRR1
    def show_reserve(self, date, state):
        sql = "select r_number,r_guest_name,r_type,r_quantity,r_price,r_guest_phone,r_arrival_date,r_departture_date " \
              "from reserve_record " \
              "where r_arrival_date = %s and r_reserve_state = %s;"
        self.cur.execute(sql, [date, state, ])
        print('8888')
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return False

    # 生成预订订单 -- RR1
    def reserve_room(self, rnum, arrival_datetime, departtuure_datetime,
                     retention_date, days, rtype, rprice, rquantity, guest_name,
                     guest_phone, rstate, rnotes, rnumber, rulog):
        sql = "select r_id from reserve_record where r_number = %s limit 1;"
        self.cur.execute(sql, [rnum, ])
        print('1212')
        # 如果查询到订单号存在
        if self.cur.fetchone():
            return False

        sql = "insert into reserve_record" \
              "(r_number, r_arrival_date, r_departture_date, " \
              "r_retention_date, r_days, r_type, r_price,r_quantity," \
              "r_guest_name, r_guest_phone, r_reserve_state, r_notes," \
              "r_room_number,r_ulog) " \
              "values " \
              "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            self.cur.execute(sql, [rnum, arrival_datetime, departtuure_datetime,
                                   retention_date, days, rtype, rprice,
                                   rquantity, guest_name, guest_phone, rstate,
                                   rnotes, rnumber, rulog])
            print('1313')
            self.db.commit()
            return True
        # 插入失败,回滚操作
        except:
            self.db.rollback()
            return False

    # 查看订单记录  -- SCR1
    def show_check(self, date, state, field_name):
        sql = "select c_order_number,guest_name,c_type,c_price,guest_phone,c_arrival_date,c_departture_date " \
              "from io_record as c left join guest_info as g on c.c_order_number = g.io_num " \
              "where {} regexp '^{}.+' and c_state = %s;".format(field_name, date)
        self.cur.execute(sql, [state, ])
        print('1414')
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return False

    # 生成入住订单  -- CIR1
    def checkin_record(self, cnum, arrival_datetime,
                       departture_datetime, days, ctype,
                       cprice, c_rnumber, cnotes, cstate, culog):

        sql = "select c_id from io_record where c_order_number = %s limit 1;"
        self.cur.execute(sql, [cnum, ])
        print('1515')
        # 如果查询到订单号存在
        if self.cur.fetchone():
            print('已存在')
            return False

        sql = "insert into io_record" \
              "(c_order_number, c_arrival_date,c_departture_date, " \
              "c_days, c_type, c_price,c_room_number,c_notes,c_state,c_ulog) " \
              "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        try:
            print('-----')
            print(cnum, arrival_datetime, departture_datetime, days, ctype, cprice, c_rnumber, cnotes, cstate, culog)
            self.cur.execute(sql, [cnum, arrival_datetime, departture_datetime,
                                   days, ctype, cprice, c_rnumber, cnotes, cstate, culog])

            print('1616')
            self.db.commit()
            return True
        # 插入失败,回滚操作
        except:
            print('回滚')
            self.db.rollback()
            return False

    # 保存客人信息 -- CGR1
    def save_guest_info(self, g_name, g_id_num, g_nationality,
                        g_sex, g_site, g_phone, g_deposit, io_num):

        sql = "select gid from guest_info where guest_id_number = %s limit 1;"
        self.cur.execute(sql, [g_id_num, ])
        print('1515')
        # 如果查询查到客人id存在，则不需要再保存客人信息
        if self.cur.fetchone():
            return True

        sql = "insert into guest_info" \
              "(guest_name, guest_id_number,guest_nationnality, " \
              "guest_sex, guest_site, guest_phone,guest_deposit,io_num) " \
              "values" \
              "(%s,%s,%s,%s,%s,%s,%s,%s);"

        try:
            self.cur.execute(sql, [g_name, g_id_num, g_nationality, g_sex,
                                   g_site, g_phone, g_deposit, io_num])

            print('1616')
            self.db.commit()
            return True
        # 插入失败,回滚操作
        except:
            self.db.rollback()
            return False

    # 退房结账，修改订单状态为退房 --COR1
    def checkout_record(self, rnumber, state):
        sql = ''
        pass

    # 查询账单 -- SRB1
    def select_bill(self, rnumber, state):
        sql = "select c_order_number,c_arrival_date,c_type,c_price,guest_name,guest_deposit " \
              "from io_record as io left join guest_info as g " \
              "on io.c_order_number = g.io_num " \
              "where c_room_number = %s and c_state = %s;"
        self.cur.execute(sql, [rnumber, state])
        print('1717')
        result = self.cur.fetchone()
        if result:
            return result[0], result[1], result[2], result[3], result[4], result[5]
        else:
            return False

    # 查看房态  --SRD1
    def show_room_dynamic(self):
        sql = 'select r_sid,group_concat(room_number),group_concat(r_tid) from room_info group by r_sid;'
        self.cur.execute(sql)
        print('1919')
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return False

    # 查看房情 -- SRA1
    # 查询各类房间总数量
    def select_room_quantity(self):
        sql = "select r_tid,count(r_sid) from room_info group by r_tid;"
        self.cur.execute(sql)
        print('2020')
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return False

    # 查询当天有效预订订单的房间数量及房型
    def select_reserve_number(self, datetime):
        # 查询当天预订订单有效房间数量及房型
        sql = " select r_type,sum(r_quantity) " \
              "from reserve_record " \
              "where r_reserve_state = 1 and r_arrival_date = %s " \
              "group by r_type;"
        self.cur.execute(sql, [datetime, ])
        print('2121')
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return '0'

    # 查询所有非当天退房订单的数量及房型
    def select_not_checkout_number(self, datetime):
        # 查询所有非当天退房订单的数量
        sql = "select c_type,count(c_order_number) " \
              "from io_record " \
              "where c_state = 1 and c_departture_date > %s" \
              " group by c_type;"

        self.cur.execute(sql, [datetime])
        print('2323')
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return '0'
