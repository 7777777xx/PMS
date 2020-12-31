"""

"""

from signal import *

from socket import *
from multiprocessing import Process
from PMS_Server.PMS_Model import Database
from PMS_Server.User_Control import *
from PMS_Server.Room_Control import *

# 服务器地址
HOST = "192.168.3.30"
PORT = 7777
ADDR = (HOST, PORT)

# 实例化数据库处理对象
db = Database()


# 处理用户登录 --L
def login(connfd, uphone, passwd):
    result = db.login(uphone, passwd)
    print(result)
    if result:
        if result[0] == "管理员":
            msg = 'ROK|%s' % result[1]
            connfd.send(msg.encode())
        else:
            msg = 'UOK|%s' % result[1]
            connfd.send(msg.encode())
    else:
        connfd.send(b"FAIL")


# 处理客户端各种请求  总分结构
def handle(connfd):
    db.create_cursor()  # 每个子进程创建自己的游标
    while True:
        # 接收某一个各类请求
        data = connfd.recv(1024).decode()
        print(data)
        # 简单解析--以|为分隔符()
        tmp = data.split('|')

        if not data or tmp[0] == 'E':
            break
        elif tmp[0] == "L":
            login(connfd, tmp[1], tmp[2])
        elif tmp[0] == "A1":
            add_user(connfd, tmp[1], tmp[2], tmp[3], tmp[4], db)
        elif tmp[0] == "D1":
            del_user(connfd, tmp[1], db)
        elif tmp[0] == "U1":
            update_user(connfd, tmp[1], tmp[2], tmp[3], db)
        elif tmp[0] == "F1":
            find_user(connfd, tmp[1], tmp[2], db)
        elif tmp[0] == "S1":
            show_user(connfd, db)
        elif tmp[0] == "SRR1":
            show_reserve_record(connfd, tmp[1], tmp[2], db)
        elif tmp[0] == "FR1":
            find_room(connfd, tmp[1], tmp[2], db)
        elif tmp[0] == "ARS1":
            alter_room_state(connfd, tmp[1], tmp[2], db)
        elif tmp[0] == "RR1":
            reserve_room(connfd, db, tmp[1], tmp[2], tmp[3],
                         tmp[4], tmp[5], tmp[6], tmp[7], tmp[8],
                         tmp[9], tmp[10], tmp[11], tmp[12], tmp[13], tmp[14])
        elif tmp[0] == "SCR1":
            show_check_record(connfd, db, tmp[1], tmp[2], tmp[3])
        elif tmp[0] == "CIR1":
            checkin_room(connfd, db, tmp[1], tmp[2], tmp[3],
                         tmp[4], tmp[5], tmp[6], tmp[7], tmp[8],
                         tmp[9], tmp[10])
        elif tmp[0] == "CGR1":
            save_ginfo(connfd, db, tmp[1], tmp[2], tmp[3],
                       tmp[4], tmp[5], tmp[6], tmp[7], tmp[8])
        elif tmp[0] == "SRB1":
            select_room_bill(connfd, db, tmp[1], tmp[2])
        elif tmp[0] == "AOS1":
            alter_order_state(connfd, db, tmp[1], tmp[2], tmp[3], tmp[4])
        elif tmp[0] == "SRD1":
            show_room_dynamic(connfd, db)
        elif tmp[0] == "SRA1":
            show_room_availability(connfd, db, tmp[1])

    db.cur.close()  # 关闭游标
    connfd.close()


def main():
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("等待客户端连接...")

    # 处理僵尸进程,windows不用
    # signal(SIGCHLD, SIG_IGN)

    while True:
        try:
            connfd, addr = sock.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            # 退出服务
            sock.close()
            db.close()
            break
        # 当有客户端连接 为客户创建进程对象
        # p = MyProcess(connfd, db)
        p = Process(target=handle, args=(connfd,))
        print('1111')
        # 客户端随服务端退出
        p.daemon = True
        print('2222')
        p.start()
        print('3333')


if __name__ == '__main__':
    main()
