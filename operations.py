from fabric import Connection

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
        command = "useradd -p "+password+" -m -d /home/"+dirname+"/ -g users -s /bin/bash "+username
        try:
            with Connection(host = ip,user = user,connect_kwargs={"password": passwd}) as conn:
                conn.sudo(command,password=passwd,hide=True).stdout.strip()
            return ('User Created: '+username,0)
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
        command = "userdel -f "+username
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