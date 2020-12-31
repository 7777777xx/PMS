"""
用户管理
"""


# 用户查询 -- F1
def find_user(sock):
    while True:
        uname = input("请输入姓名：")
        uphone = input("请输入手机号：")
        if " " in uname or " " in uphone:
            print("姓名和手机号格式不正确")
            continue
        # 组织请求
        msg = "F1|%s|%s" % (uname, uphone)
        sock.send(msg.encode())
        # 等待结果
        result = sock.recv(1024).decode()
        result = eval(result)
        print("用户查询 -- F1", result)
        # 分情况讨论：
        if result[0] == "F1OK":
            print("""
                            +-----------+------------+----------------+-----------+
                            |     id    |    姓名     |     手机号      |    职位    |
                            +-----------+------------+----------------+-----------+
                        """)

            print("""
                            |    %s    |  %s  |  %s  |   %s    | 
                            """ % (result[1], result[2], result[3], result[4]))

            print("""
                            +-----------+------------+-----------------+----------+
                        """)
            return result[1]

        else:
            print("该用户不存在")
            return False


# 用户添加 -- A1
def add_user(sock):
    while True:
        uname = input("请输入姓名(2键退出添加)：")
        if uname == "2":
            return
        uphone = input("请输入手机号：")
        passwd = input("请设置密码：")
        position = input("请输入职位：")
        if not uname or not uphone or not passwd or not position:
            print("------请输入内容-------")
            continue
        if " " in uname or " " in uphone or " " in passwd or " " in position:
            print("输入内容不许有空格,请重新输入")
            continue

        # 组织请求
        msg = "A1|%s|%s|%s|%s" % (uname, uphone, passwd, position)
        sock.send(msg.encode())
        # 等待结果
        result = sock.recv(1024).decode()
        print("用户添加 -- A1", result)
        # 分情况讨论：
        if result == "A1OK":
            print("添加成功")
        else:
            print("该用户已存在")
        return


# 用户删除 -- D1
def del_user(sock):
    result = find_user(sock)
    if result:
        option = input("是否确认删除（Y键确认，任意键退出）：")
        if option == "Y":
            msg = "D1|%s" % result
            sock.send(msg.encode())
            print("用户删除 -- D1", result)
            data = sock.recv(1024).decode()
            # 分情况讨论：
            if data == "D1OK":
                print("删除成功")
            else:
                print("网络错误")
            return
        else:
            return
    else:
        return


# 用户修改 -- U1
def update_user(sock):
    result = find_user(sock)
    if result:
        while True:
            print("""
                    ╔==========用户修改==========╗
          
                             1> 修改姓名             
                             2> 修改密码              
                             3> 修改职位              
                             4> 修改手机号
                             0> 退出                          
        
                    ╚===========================╝
            """)
            cmd = input("请输入选项：")
            if cmd == "1":
                new_name = input("姓名修改为：")
                if " " in new_name or not new_name:
                    print("姓名格式不正确，请重新输入")
                    continue
                msg = "U1|user_name|%s|%s" % (new_name, result)
                sock.send(msg.encode())
                data = sock.recv(1024).decode()
                if data == "U1OK":
                    print("修改成功")
                    return
                else:
                    print("修改失败，请检查修改内容")
                    continue

            elif cmd == "2":
                # new_password = input("密码修改为：")
                # if " " in new_password or not new_password:
                #     print("密码格式不正确，请重新输入")
                #     continue
                # msg = "U1|password  %s|%s" % (new_password, result)
                # sock.send(msg.encode())
                # data = sock.recv(1024).decode()
                # print(data)
                # if data == "U1OK":
                #     print("修改成功")
                #     return
                # else:
                #     print("修改失败，请检查修改内容")
                #     continue
                alter_password(sock, result)

            elif cmd == "3":
                new_position = input("职位修改为：")
                if " " in new_position or not new_position:
                    print("职位格式不正确，请重新输入")
                    continue
                msg = "U1|position|%s|%s" % (new_position, result)
                sock.send(msg.encode())
                data = sock.recv(1024).decode()
                if data == "U1OK":
                    print("修改成功")
                    return
                else:
                    print("修改失败，请检查修改内容")
                    continue

            elif cmd == "4":
                new_phone = input("手机号修改为：")
                if " " in new_phone or not new_phone:
                    print("手机号格式不正确，请重新输入")
                    continue
                msg = "U1|user_phone|%s|%s" % (new_phone, result)
                sock.send(msg.encode())
                data = sock.recv(1024).decode()
                if data == "U1OK":
                    print("修改成功")
                    return
                else:
                    print("修改失败，请检查修改内容")
                    continue

            elif cmd == "0":
                return
            else:
                print("未知命令，请重新输入")
                continue


# 普通用户修改密码
def alter_password(sock, uid):
    new_password = input("密码修改为：")
    if " " in new_password or not new_password:
        print("密码格式不正确，请重新输入")
        return
    msg = "U1|password|%s|%s" % (new_password, uid)
    sock.send(msg.encode())
    data = sock.recv(1024).decode()
    print(data)
    if data == "U1OK":
        print("修改成功,请重新登录")
    else:
        print("修改失败，请检查修改内容")
    return


# 显示所有用户 -- S1
def show_user(sock):
    sock.send(b"S1")
    print("""
                +-----------+------------+----------------+-----------+
                |     id    |    姓名     |     手机号      |    职位    |
                +-----------+------------+----------------+-----------+
            """)
    while True:
        data = sock.recv(1024).decode()
        # print(data)
        result = data.split('|')
        # print(result)
        if data == "##":
            break

        print("""
                |    %s      |   %s    | %s   |   %s     | 
         """ % (result[0], result[1], result[2], result[3]))

        print("""
                +-----------+------------+-----------------+----------+
        """)
