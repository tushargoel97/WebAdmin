from invoke import Responder
from fabric import Connection

class OperationsUtil():
    def __init__(self):
        self.rootUser="ubuntu20"
        self.rootPass="VMware123!"
        self.conn=Connection(host='ubuntu20@10.109.34.222',connect_kwargs={"password": self.rootPass})
    def createUser(self, username, password, dirname):
        if not dirname:
            dirname = username
        command = "useradd -p "+password+" -m -d /home/"+dirname+"/ -g users -s /bin/bash "+username
        try:
            val = self.conn.sudo(command,password=self.rootPass,hide=True).stdout.strip()
            return ('User Created: '+username,0)
        except Exception as e:
            return ('Cannot create user',1)

    def viewUser(self):
        command = "awk -F: '{ print $1}' /etc/passwd"
        return self.conn.run(command,hide=True).stdout.strip()

    def deluser(self,username):
        command = "userdel -f "+username
        try:
            val = self.conn.sudo(command,password=self.rootPass,hide=True).stdout.strip()
            return ('User Deleted: '+username,0)
        except Exception as e:
            return ('Cannot delete user',1)

    def updatePriv(self,username):
        command = "usermod -aG sudo "+username
        try:
            val = self.conn.sudo(command,password=self.rootPass).stdout.strip()
            return ('User Privilege Granted',0)
        except Exception as e:
            return ('Cannot Grant user Privileges',1)

op = OperationsUtil()
# print(op.createUser("test", "test")[0])
# print(op.viewUser())
# print(op.updatePriv("test")[0])
print(op.deluser("test1")[0])