from flask import Flask, render_template, request, session, redirect, abort
import config
import pymysql

app = Flask(__name__)

app.config["SECRET_KEY"] = config.SECRET_KEY



# ___________________start database products___________________ #
def database():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",
    )
    cursor = conn.cursor()

    cursor.execute("CREATE SCHEMA IF NOT EXISTS `mtr_shop`")
    cursor.execute("CREATE TABLE `mtr shop`.`products` (\
  `id` INT NOT NULL AUTO_INCREMENT,\
  `name` VARCHAR(200) NOT NULL,\
  `prce` INT NULL,\
  `description` TEXT NULL,\
  `active` INT NULL,\
  `productscol` VARCHAR(45) NULL,\
  PRIMARY KEY (`id`),\
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);")
    conn.commit()


database()
# ___________________end database products___________________ #






# ___________________start route home or page home___________________ #
@app.route("/")
def home():
    return render_template("home.html")


# ___________________end route home or page home___________________ #








# ___________________start route /admin/login or page admin login___________________ #
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username_admin", None)
        password = request.form.get("password_admin", None)
        if username == config.USERNAME_ADMIN and password == config.PASSWORD_ADMIN:
            session["admin_login"] = username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    return render_template("admin_login.html")
# ___________________end route /admin/login or page admin login___________________ #




# ___________________start route /admin/dashboard or page dashboard admin___________________ #
@app.route("/admin/dashboard", methods=["GET"])
def dashboard():
    if session.get("admin_login", None) == None:
        abort(403)
# ___________________end route /admin/dashboard or page dashboard admin___________________ #

if __name__ == "__main__":
    app.run(debug=True)
