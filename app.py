from flask import Flask, render_template, request, session, redirect, abort
import config
import pymysql
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = config.SECRET_KEY




# ___________________start database products___________________ #
def products():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",
    )
    cursor = conn.cursor()

    cursor.execute("CREATE SCHEMA IF NOT EXISTS `mtr_shop`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `mtr_shop`.`products` (\
  `id` INT NOT NULL AUTO_INCREMENT,\
  `name` VARCHAR(200) NOT NULL,\
  `prce` INT NULL,\
  `description` TEXT NULL,\
  `active` VARCHAR(5) NULL,\
  PRIMARY KEY (`id`),\
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);")
    conn.commit()
# ___________________end database products___________________ #


# ___________________start database users___________________ #
def users():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS`mtr_shop`.`users` (\
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
  `username` VARCHAR(200) NOT NULL,\
  `password` VARCHAR(200) NOT NULL,\
  `phone` VARCHAR(50) NOT NULL,\
  `address` VARCHAR(600) NULL,\
  PRIMARY KEY (`id`),\
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,\
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);")
    conn.commit()
# ___________________end database users___________________ #

        
        
        
        
#__ create database__ # 
products()
users()
#__ create database__ #   





def connection_db():
        return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root"
        )

# ______________________________________________✔✔start code admin✔✔______________________________________________ #



# ___________________start route home or page home___________________ #
@app.route("/")
def home():
    conn = connection_db()
    cursor = conn.cursor()
    sql_insert = "SELECT * FROM mtr_shop.products WHERE active = 'on';"
    cursor.execute(sql_insert)
    all_products = cursor.fetchall()
    return render_template("home.html" , namepage = config.name_page_home , all_products = all_products)


# ___________________end route home or page home___________________ #


# ___________________start route /products/... or page products___________________ #
@app.route("/products/<int:id>/<name>")
def products(id, name):
    conn = connection_db()
    cursor = conn.cursor()
    sql_insert = "SELECT * FROM mtr_shop.products WHERE id = %s and name = %s;"
    cursor.execute(sql_insert,(id , name))
    one_products = cursor.fetchone()
    return render_template('view_products.html' , one_products = one_products)



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
    return render_template("admin/admin_login.html", namepage = config.name_page_admin_login)
# ___________________end route /admin/login or page admin login___________________ #






# ___________________start route /admin/dashboard or page dashboard admin___________________ #
@app.route("/admin/dashboard", methods=["GET"])
def dashboard():
    if session.get("admin_login", None) == None:
        abort(403)
    return render_template('admin/dashboard.html' , namepage = config.name_page_dashboard)
# ___________________end route /admin/dashboard or page dashboard admin___________________ #







# ___________________start route /admin/dashboard/products or page products admin___________________ #
@app.route("/admin/dashboard/admin-products", methods=["GET","POST"])
def admin_products():    
    if session.get("admin_login", None) == None:
        abort(403)
    conn = connection_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name  = request.form.get('name')
        prce  = request.form.get('prce')
        description  = request.form.get('description')
        active  = request.form.get('active')
        image = request.files.get('image')
        if active == None:
            active = 'off'
        sql_insert = "INSERT INTO `mtr_shop`.`products` (`name`, `prce`, `description`, `active`) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql_insert , (name  , prce , description , active))
        conn.commit()
        product_id = cursor.lastrowid
        image.save(f'./static/imagesProducts/{product_id}.jpg')
    sql_select = "SELECT * FROM mtr_shop.products;"
    cursor.execute(sql_select)
    all_products = cursor.fetchall()
        
    return render_template('admin/products.html' , namepage = config.name_page_products , all_products = all_products)
# ___________________end route /admin/dashboard/products or page products admin___________________ #





# ___________________start route /admin/dashboard/edit-products/... or page edit product___________________ #

@app.route("/admin/dashboard/edit-products/<int:id>", methods=["GET","POST"])
def edit_products(id):
    if session.get("admin_login", None) == None:
        abort(403) 
    conn = connection_db()
    cursor = conn.cursor()
    sql_insert = "SELECT * FROM mtr_shop.products where id = %s;"
    cursor.execute(sql_insert , id)
    one_products = cursor.fetchone()
    conn.commit()
    if request.method == 'POST':
        name = request.form.get('name')
        prce = request.form.get('prce')
        description = request.form.get('description')
        active = request.form.get('active')
        image = request.files.get('image')
        if active == None:
            active = 'off'
        sql_update = "UPDATE `mtr_shop`.`products` SET `name` = %s WHERE (`id` = %s );"
        sql_update1 = "UPDATE `mtr_shop`.`products` SET `prce` = %s WHERE (`id` = %s );"
        sql_update2 = "UPDATE `mtr_shop`.`products` SET `description` = %s WHERE (`id` = %s );"
        sql_update3 = "UPDATE `mtr_shop`.`products` SET `active` = %s WHERE (`id` = %s );"
        cursor.execute(sql_update,(name,id)) 
        cursor.execute(sql_update1,(prce,id)) 
        cursor.execute(sql_update2,(description,id)) 
        cursor.execute(sql_update3,(active ,id)) 
        conn.commit()
        if image and image.filename != '':
            image.save(f'./static/imagesProducts/{one_products[0]}.jpg')
    return render_template('admin/edit-products.html' , one_products = one_products , namepage = config.name_page_editproducts)
# __________________end route /admin/dashboard/edit-products/... or page edit product___________________ #


# ___________________start route /admin/dashboard/delete-products/... or page delete product___________________ #
@app.route("/admin/dashboard/delete-products/<int:id>", methods=["GET","POST"])
def delete_products(id):
    if session.get("admin_login", None) == None:
        abort(403) 
    conn = connection_db()
    cursor = conn.cursor()
    if request.method == 'GET':
        image_filename = f"{id}.jpg"
        image_path = os.path.join('static', 'imagesProducts', image_filename)
        os.remove(image_path)
        sql_delete = "DELETE FROM `mtr_shop`.`products` WHERE (`id` = %s );"
        cursor.execute(sql_delete,(id)) 
        conn.commit()
    return redirect('/admin/dashboard/admin-products')
# ___________________end route /admin/dashboard/delete-products/... or page delete product___________________ #




# ______________________________________________✔✔end code admin✔✔______________________________________________ #



####################################################################################################################
####################################################################################################################
####################################################################################################################




# ______________________________________________✔✔start code users✔✔______________________________________________ #


@app.route('/sign-up' , methods = ["GET" , "POST"])
def sign_up():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        conn = connection_db()
        cursor = conn.cursor()
        sql_insert = "INSERT INTO `mtr_shop`.`users` (`username`, `password`, `phone`, `address`) VALUES (%s,%s,%s,%s);"
        cursor.execute(sql_insert , (username, password, phone, address))
        conn.commit()
    
    
    return render_template('users/sign_up.html', namepage = config.name_page_sign_up)

@app.route('/log-in')
def login():

    return render_template('users/login.html', namepage = config.name_page_login)

if __name__ == "__main__":
    app.run(debug=True)