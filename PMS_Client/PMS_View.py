"""


"""

from socket import *
from PMS_Client.User import *
from PMS_Client.Room import *
import sys

# 服务器地址
ADDR = ("192.168.3.30", 7777)


class PmsView:
    def __init__(self, sockfd):
        self.scokfd = sockfd

    # 一级界面
    def one_interfase(self):
        while True:
            print("""
            ======= welcome ========                  
               1. 登录      2. 退出          
            ======================== 
            """)
            cmd = input("请输入命令：")
            if cmd == "1":
                self.login()
            elif cmd == "2":
                self.scokfd.send(b"E")
                self.scokfd.close()
                break
            else:
                print("命令错误")

    # root用户二级界面
    def root_two_interfase(self, user_name):
        while True:
            print(
                """
                ╔==========用户管理==========╗
    
    
                         1> 用户添加              
                         2> 用户删除              
                         3> 用户修改              
                         4> 用户查询
                         5> 显示所有用户信息              
    
                    9>注销         0> 退出                
    
                 ╚==========  %s  =========╝
                """ % user_name
            )
            cmd = input("请输入命令:：")
            if cmd == "1":
                add_user(self.scokfd)
            elif cmd == "2":
                del_user(self.scokfd)
            elif cmd == "3":
                update_user(self.scokfd)
            elif cmd == "4":
                find_user(self.scokfd)
            elif cmd == "5":
                show_user(self.scokfd)
            elif cmd == "9":
                self.one_interfase()
                break
            elif cmd == "0":
                self.scokfd.send(b"E")
                self.scokfd.close()
                sys.exit()

            else:
                print("未知命令")

    # 普通用户的二级界面
    def user_two_interfase(self, user_name):
        while True:
            print(
                """
                ╔==========用户管理==========╗
    
    
                         1> 预定              
                         2> 入住              
                         3> 退房              
                         4> 查看房情
                         5> 查看房态
                         6> 修改房态
                         7> 修改密码
                                       
    
                    9>注销         0> 退出                
    
                ╚===========  %s  =========╝
                """ % user_name
            )
            cmd = input("请输入命令：")
            if cmd == "1":
                self.reserve(user_name)
            elif cmd == "2":
                self.checkin(user_name)
            elif cmd == "3":
                self.checkout(user_name)
            elif cmd == "4":
                show_room_availability(self.scokfd, user_name)
            elif cmd == "5":
                show_room_dynamic(self.scokfd, user_name)
            elif cmd == "6":
                alter_rstate(self.scokfd)
            elif cmd == "7":
                uid = find_user(self.scokfd)
                alter_password(self.scokfd, uid)
                break
            elif cmd == "9":
                break
            elif cmd == "0":
                self.scokfd.send(b"E")
                self.scokfd.close()
                sys.exit()

            else:
                print("未知命令")

    # -------------------------------------------------------------------------------
    # 普通用户的三级界面
    # 预订
    def reserve(self, user_name):
        while True:
            print(
                """
                ╔=====  预订  =====╗

                    1> 查看预订列表              
                    2> 预订房间              
                    3> 退出              

                ╚==================╝
                """
            )
            cmd = input("请输入命令：")
            if cmd == "1":
                show_reserve_record(self.scokfd)
            elif cmd == "2":
                reserve_room(self.scokfd, user_name)
            elif cmd == "3":
                break
            else:
                print("未知命令")

    # 入住
    def checkin(self, user_name):
        while True:
            print(
                """
                ╔=====  预订  =====╗

                    1> 查看入住列表              
                    2> 入住房间              
                    3> 退出              

                ╚==================╝
                """
            )
            cmd = input("请输入命令：")
            if cmd == "1":
                show_checkin_record(self.scokfd)
            elif cmd == "2":
                checkin_room(self.scokfd, user_name)
            elif cmd == "3":
                break
            else:
                print("未知命令")

    # 退房
    def checkout(self, user_name):
        while True:
            print(
                """
                ╔=====  预订  =====╗

                    1> 查看退房列表              
                    2> 退房结账              
                    3> 退出              

                ╚==================╝
                """
            )
            cmd = input("请输入命令：")
            if cmd == "1":
                show_checkout_record(self.scokfd)
            elif cmd == "2":
                checkout_room(self.scokfd, user_name)
            elif cmd == "3":
                break
            else:
                print("未知命令")

    # 登录
    def login(self):
        i = 0
        while i < 5:
            uphone = input("请输入帐号（2键退出）：")
            if uphone == "2":
                return
            passwd = input("请输入密码：")

            msg = "L|%s|%s" % (uphone, passwd)
            self.scokfd.send(msg.encode())
            data = self.scokfd.recv(128).decode()
            result = data.split("|")
            # print(result)
            if result[0] == "ROK":
                print("登录成功")
                self.root_two_interfase(result[1])
            elif result[0] == "UOK":
                print("登录成功")
                self.user_two_interfase(result[1])
            else:
                print("用户名或密码错误")
        else:
            print("登录失败，请稍后登录")


# 启动服务
def main():
    # 连接服务端
    sockfd = socket()
    sockfd.connect(ADDR)
    pms = PmsView(sockfd)
    pms.one_interfase()


if __name__ == '__main__':
    main()
