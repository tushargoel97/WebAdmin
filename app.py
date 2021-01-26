from flask import Flask, render_template, request, session, redirect, url_for
from operations import OperationsUtil
app = Flask(__name__)

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
            return render_template('message.html', message="Invalid Credentials", color='red')
        
        validIP = list(filter(lambda x:x>0 and x<255, [int(x) for x in system_ip.split(".")]))
        
        if len(validIP)!=4:
            return render_template('message.html', message="Invalid IP Address", color='red')

        result = OperationsUtil.tryConnection(system_ip, username, password)
        
        session['system_ip'] = system_ip
        session['username'] = username
        session['password'] = password
        return redirect(url_for('operations'))
    except Exception as e:
        return render_template('message.html', message='Invalid Credentials', color='red')

@app.route('/operations', methods=['GET'])
def operations():
    try:
        a = session['system_ip']
        b = session['username']
        c = session['password']
        return render_template('operations.html')
    except Exception as e:
        return render_template('message.html', message='Invalid Session', color='red')

@app.route('/create', methods=['GET', 'POST'])
def createUser():
    if request.method=='POST':
        try:
            username = str(request.form['username'])
            password = str(request.form['password'])
            dirname = str(request.form['dirname'])
            result = OperationsUtil.createUser(session['system_ip'], session['username'], session['password'], username, password, dirname)
            if result[1]==1:
                return render_template('message.html', message=result[0], color='red')
            else:
                return render_template('message.html', message=result[0], color='green')
        except Exception as e:
            return render_template('message.html', message='Invalid Credentials', color='red')
    else:
        try:
            a = session['system_ip']
            b = session['username']
            c = session['password']
            return render_template('create_user.html')
        except Exception as e:
            return render_template('message.html', message='Invalid Session', color='red')

@app.route('/view', methods=['GET'])
def viewUser():
    try:
        result = OperationsUtil.viewUser(session['system_ip'], session['username'], session['password'])
        if result[1]==1:
            return render_template('message.html', message=result[0], color='red')
        else:
            users = result[0].split("\n")
            return render_template('view_user.html',users=users)
    except Exception as e:
        return render_template('message.html', message='Invalid Session', color='red')
    

@app.route('/assign-privilege', methods=['GET', 'POST'])
def updateUser():
    if request.method=='POST':
        try:
            username = str(request.form['username'])
            result = OperationsUtil.updatePriv(session['system_ip'], session['username'], session['password'], username)
            if result[1]==0:
                return render_template('message.html', message=result[0], color='green')
            else:
                return render_template('message.html', message=result[0], color='red')
        except Exception as e:
            return render_template('message.html', message='Invalid Session', color='red')
    else:
        try:
            a = session['system_ip']
            b = session['username']
            c = session['password']
            return render_template('update_user.html')
        except Exception as e:
            return render_template('message.html', message='Invalid Session', color='red')

@app.route('/delete', methods=['GET', 'POST'])
def deleteUser():
    if request.method=='POST':
        try:
            username = str(request.form['username'])
            result = OperationsUtil.deluser(session['system_ip'], session['username'], session['password'], username)
            if result[1]==0:
                return render_template('message.html', message=result[0], color='green')
            else:
                return render_template('message.html', message=result[0], color='red')
        except Exception as e:
            return render_template('message.html', message='Invalid Session', color='red')
    else:
        try:
            a = session['system_ip']
            b = session['username']
            c = session['password']
            return render_template('delete_user.html')
        except Exception as e:
            return render_template('message.html', message='Invalid Session', color='red')

if __name__ == '__main__':
    app.run()