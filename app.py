from flask import Flask,render_template,request,session,redirect,abort
import config
app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin/login' , methods = ['GET' , 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username_admin' , None)
        password = request.form.get('password_admin' , None)
        if username == config.USERNAME_ADMIN and password == config.PASSWORD_ADMIN:
            session['admin_login'] = username
            return redirect('/admin/dashboard')
        else:
            return redirect('/admin/login')
    return render_template('admin_login.html')



@app.route('/admin/dashboard' , methods = ['GET'])
def dashboard():
    if session.get('admin_login' , None) == None:
        abort(403)

if __name__ == '__main__':
    app.run(debug = True)
    