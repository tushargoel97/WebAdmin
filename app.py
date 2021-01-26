from flask import Flask, render_template, request, session
from .operations import OperationsUtil
app = Flask(__name__)

# app.config.from_object('config.Config')
app.config['SECRET_KEY'] = '*gvb_)uc+@xdr@+e%@bzc^i24uw)@_hl26q2+ihv4gd9e2oy-g'

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/connect', methods=['POST'])
def connectToMachine():
    try:
        system_ip = str(request.form['system_ip'])
        username = str(request.form['username'])
        password = str(request.form['password'])

        if not system_ip or not username or not password:
            return render_template('error.html', message="Invalid Credentials")
        
        validIP = list(filter(lambda x:x>0 and x<255, [int(x) for x in system_ip.split(".")]))
        
        if len(validIP)!=4:
            return render_template('error.html', message="Invalid Credentials")
        
        if OperationsUtil.tryConnection(system_ip, username, password)!=0:
            raise Exception('Invalid')
        
        session['system_ip'] = system_ip
        session['username'] = username
        session['password'] = password
        return render_template('operations.html')
    except Exception as e:
        return render_template('error.html', message='Invalid Credentials')

@app.route('/create', methods=['GET', 'POST'])
def createUser():
    if request.method=='POST':
        try:
            username = str(request.form['username'])
            password = str(request.form['password'])
            dirname = str(request.form['dirname'])
            result = OperationsUtil.createUser(session['system_ip'], session['username'], session['password'], username, password, dirname)
            if result[1]==1:
                return render_template('error.html', message=result[0])
            else:
                return render_template('success.html', message=result[0])
        except Exception as e:
            return render_template('error.html', message='Invalid Credentials')
    else:
        return render_template('create_user.html')

@app.route('/view', methods=['GET'])
def viewUser():
    try:
        result = OperationsUtil.viewUser(session['system_ip'], session['username'], session['password'])
        if result[1]==1:
            return render_template('error.html', message=result[0])
        else:
            users = result[0].split("\n")
            return render_template('view_user.html',users=users)
    except Exception as e:
        return render_template('error.html', message='Connection Invalid')
    

@app.route('/assign-privilege', methods=['GET', 'POST'])
def updateUser():
    if request.method=='POST':
        try:
            username = str(request.form['username'])
            result = OperationsUtil.updatePriv(session['system_ip'], session['username'], session['password'], username)
            if result[1]==0:
                return render_template('success.html', message=result[0])
            else:
                return render_template('error.html', message=result[0])
        except Exception as e:
            return render_template('error.html', message='Connection Invalid')
    else:
        return render_template('update_user.html')

@app.route('/delete', methods=['GET', 'POST'])
def deleteUser():
    if request.method=='POST':
        try:
            username = str(request.form['username'])
            result = OperationsUtil.deluser(session['system_ip'], session['username'], session['password'], username)
            if result[1]==0:
                return render_template('success.html', message=result[0])
            else:
                return render_template('error.html', message=result[0])
        except Exception as e:
            return render_template('error.html', message='Connection Invalid')
    else:
        return render_template('delete_user.html')

if __name__ == '__main__':
    app.run()