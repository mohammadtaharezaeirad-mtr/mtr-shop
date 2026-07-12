from flask import Flask, render_template, request, session, redirect, abort , url_for
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

def cart():
    conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `mtr_shop`.`cart` (\
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
  `user_id` INT UNSIGNED NOT NULL,\
  `product_id` INT NOT NULL,\
  `quantity` INT NOT NULL,\
  PRIMARY KEY (`id`),\
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,\
  INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE,\
  UNIQUE INDEX `product_id_UNIQUE` (`product_id` ASC) VISIBLE,\
  CONSTRAINT `id user`\
    FOREIGN KEY (`user_id`)\
    REFERENCES `mtr_shop`.`users` (`id`)\
    ON DELETE CASCADE\
    ON UPDATE CASCADE,\
  CONSTRAINT `id product`\
    FOREIGN KEY (`product_id`)\
    REFERENCES `mtr_shop`.`products` (`id`)\
    ON DELETE CASCADE\
    ON UPDATE CASCADE);")

        
        
#__ create database__ # 
products()
users()
cart()
#__ create database__ #   





def connection_db():
        return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database='mtr_shop'
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
@app.route("/products/<int:id>/<name>" , methods = ['POST' , 'GET'])
def products(id, name):
    conn = connection_db()
    cursor = conn.cursor()
    sql_insert = "SELECT * FROM mtr_shop.products WHERE id = %s and name = %s;"
    cursor.execute(sql_insert,(id , name))
    one_products = cursor.fetchone()
    return render_template('view_products.html' , one_products = one_products ,namepage = config.name_page_view_products)



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
        sql_update = "UPDATE `mtr_shop`.`products` SET `name` = %s ,`prce` = %s , `description` = %s , `active` = %s WHERE (`id` = %s );"
        cursor.execute(sql_update,(name,prce,description,active,id)) 
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





# ___________________start route /sign-up or page sign up user___________________ #
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
        return redirect('/log-in')
    
    return render_template('users/sign_up.html', namepage = config.name_page_sign_up)
# ___________________end route /sign-up or page sign up user___________________ #



# ___________________start route /log-in or page log in user___________________ #
@app.route('/log-in' , methods = ['POST' , 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username_user')
        password = request.form.get('password_user')
        conn = connection_db()
        cursor = conn.cursor()
        
        sql_result = 'SELECT * FROM mtr_shop.users where username = %s and password = %s;'
        cursor.execute(sql_result , (username , password))
        one_user = cursor.fetchone()
        if one_user == None:
            return render_template('users/login.html' , error = 'نام کاربری یا پسورد یا درست وارد کند' , namepage = config.name_page_login)
        session["user_id"] = one_user[0]
    return render_template('users/login.html', namepage = config.name_page_login)
# ___________________end route /log-in or page log in user___________________ #

@app.route('/product/cart' , methods = ['POST' , 'GET'])
def cart():
    conn = connection_db()
    cursor = conn.cursor()
    user_id = session.get('user_id')
    if request.method == 'POST':
        product_id = request.form.get('product')
        quantity = request.form.get('quantity')
        if user_id == None:
            return redirect('/log-in')
        sql_insert = 'INSERT INTO `mtr_shop`.`cart` (`user_id`, `product_id` , `quantity`) VALUES (%s , %s , %s);'
        cursor.execute(sql_insert , (user_id , product_id , quantity))
        conn.commit()
        return render_template('cart_user.html')
    sql_result = """
        SELECT p.*
        FROM cart
        JOIN products p ON cart.product_id = p.id
        WHERE cart.user_id = %s;
    """
    cursor.execute(sql_result,(user_id))
    conn.commit()
    allUser_product = cursor.fetchall()
    print(allUser_product)
    return render_template('cart_user.html' , allUser_product = allUser_product)

if __name__ == "__main__":
    app.run(debug=True)