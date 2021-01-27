from fabric import Connection
from invoke import Responder

class OperationsUtil():
    @staticmethod
    def tryConnection(ip, user, passwd):
        with Connection(host = ip,user = user,connect_kwargs={"password": passwd}) as conn:
            conn.run('uname -s')
        return 0

    @staticmethod
    def createUser(ip, user, passwd, username, password, dirname=None):
        if not dirname:
            dirname = username
        
        responder = Responder(
            pattern=r'(Retype)?(N|n)?ew password:',
            response=f'{password}\n',
        )
        command = "useradd -m -d /home/"+dirname+"/ -g users -s /bin/bash "+username
        passwdCmd = "passwd "+username
        try:
            with Connection(host = ip,user = user,connect_kwargs={"password": passwd}) as conn:
                conn.sudo(command,password=passwd,hide=True).stdout.strip()
                val2 = conn.sudo(passwdCmd,password=passwd,hide=True,watchers = [responder]).exited
            if val2==0:
                return ('User Created: '+username,0)
            else:
                return ('Cannot create user',1)
        except Exception as e:
            return ('User already Exists',1)

    @staticmethod
    def viewUser(ip, user, passwd):
        command = "awk -F: '{ print $1}' /etc/passwd"
        try:
            with Connection(host = ip,user = user,connect_kwargs={"password": passwd}) as conn:
                val = conn.run(command,hide=True).stdout.strip()
            return (val, 0)
        except Exception as e:
            return ('Cannot get users',1)

    @staticmethod
    def deluser(ip, user, passwd, username):
        command = "userdel -rf "+username
        try:
            with Connection(host = ip,user = user,connect_kwargs={"password": passwd}) as conn:
                conn.sudo(command,password=passwd,hide=True).stdout.strip()
            return (username+' User deleted', 0)
        except Exception as e:
            return ("User doesn't Exists", 1)

    @staticmethod
    def updatePriv(ip, user, passwd, username):
        command = "usermod -aG sudo "+username
        try:
            with Connection(host = ip,user = user,connect_kwargs={"password": passwd}) as conn:
                conn.sudo(command,password=passwd).stdout.strip()
            return ('User Privilege Granted',0)
        except Exception as e:
            return ('Cannot Grant user Privileges',1)