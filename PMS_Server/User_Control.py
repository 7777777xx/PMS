"""
用户管理

"""

from time import sleep


# 处理用户查询 -- F1
def find_user(connfd, uname, uphone, db):
    result = db.find_user(uname, uphone)
    print(result)
    if result:
        msg = ("F1OK",) + result
        print(msg)
        connfd.send(str(msg).encode())
    else:
        msg = ("FAIL",)
        print(msg)
        connfd.send(str(msg).encode())


# 处理用户添加 -- A1
def add_user(connfd, uname, uphone, passwd, position, db):
    if db.add_user(uname, uphone, passwd, position):
        connfd.send(b"A1OK")
    else:
        connfd.send(b"FAIL")


# 处理用户删除 -- D1
def del_user(connfd, uid, db):
    if db.del_user(uid):
        connfd.send(b"D1OK")
    else:
        connfd.send(b"FAIL")


# 处理用户修改 -- U1
def update_user(connfd, field_name, info, uid, db):
    if field_name == "password":
        if db.update_passwd(info, uid):
            connfd.send(b"U1OK")
        else:
            connfd.send(b"FAIL")
    else:
        if db.update_user(field_name, info, uid):
            connfd.send(b"U1OK")
        else:
            connfd.send(b"FAIL")


# 处理显示所有用户 -- S1
def show_user(connfd, db):
    result = db.show_user()
    print(result)
    for user in result:
        print(user)
        msg = "%s|%s|%s|%s" % user
        print(msg)

        connfd.send(msg.encode())
        sleep(0.1)
    connfd.send(b"##")
