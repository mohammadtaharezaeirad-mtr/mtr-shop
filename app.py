from flask import Flask,render_template,request,session,redirect,abort
import config
import pymysql
app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY


def database():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",  
        )
    cursor = conn.cursor()
    
    
    cursor.execute("CREATE SCHEMA IF NOT EXISTS `mtr shop`")
    cursor.execute("CREATE TABLE IF NOT EXISTS`mtr_shop`.`login_user` (\
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
  `username` VARCHAR(200) NOT NULL,\
  `password` VARCHAR(45) NOT NULL,\
  PRIMARY KEY (`id`),\
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,\
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,\
  UNIQUE INDEX `password_UNIQUE` (`password` ASC) VISIBLE);")
    conn.commit()
    

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
    database()
    