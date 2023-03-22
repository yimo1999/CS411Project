import sqlalchemy
from flask import Flask, flash, session, redirect, url_for, render_template
from flask import request, jsonify
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user
from flask_session import Session


import threading
from threading import Thread
app = Flask(__name__)
i = 0
lock = threading.Lock()

app.secret_key = '1234567'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


app.config['SESSION_TYPE'] = 'filesystem'  # session类型为redis
app.config[
    'SESSION_FILE_DIR'] = 'C:/Users/S1mple/PycharmProjects/Ore_bot/CS411 Project/session'  # session类型为redis
app.config['SESSION_FILE_THRESHOLD'] = 2  # 存储session的个数如果大于这个值时，就要开始进行删除了
app.config['SESSION_FILE_MODE'] = 384  # 文件权限类型

app.config['SESSION_PERMANENT'] = True  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀

Session(app)
@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id

        return curr_user

users = [
    {'id':'Tom', 'username': 'Tom', 'password': '111111'},
    {'id':'Michael', 'username': 'Michael', 'password': '123456'},
    {'id':'a', 'username': 'a', 'password': 'a'}

]


class User(UserMixin):
    pass


def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user


@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        # username = request.form.get('username')
        # pwd = request.form.get('password')
        username = data['username']
        # pwd = data['password']
        db = init_connection_engine()
        conn = db.connect()
        sql = 'select * from Account where username = "{}"'.format(username)
        query_results = conn.execute(sql).fetchall()
        if len(query_results):
            return 'duplicate user'
        sql = 'insert into Account(username, password) values("{}", "{}");'.format(username, "111")
        conn.execute(sql)
        conn.close()
        # login.html not create
        return render_template('login.html')
    else:
        # login.html not create
        return render_template('signup.html')


@app.route("/ChangePassword", methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        data = request.get_json()

        # username = request.form.get('username')
        # pwd = request.form.get('password')
        username = data['username']
        pwd = data['password']
        db = init_connection_engine()
        conn = db.connect()
        sql = 'select * from Account where username = "{}"'.format(username)
        query_results = conn.execute(sql).fetchall()
        if len(query_results):
            sql = 'update Account set password = "{}" where username = "{}"'.format(pwd, username)
            conn.execute(sql)
            conn.close()
            # login.html not create
            # show change password success
            return render_template('login.html')
        else:
            # ChangePassword.html note create
            # show user not exist, try again
            return render_template('ChangePassword.html')


@app.route("/deleteUser", methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        data = request.get_json()
        # username = request.form.get('username')
        # pwd = request.form.get('password')
        username = data['username']
        pwd = data['password']
        db = init_connection_engine()
        conn = db.connect()
        # sql = 'select password from Account where username = "{}"'.format(username)
        # query_results = conn.execute(sql).fetchall()
        # for res in query_results:
        sql = 'delete from Account where username = "{}"'.format(username)
        conn.execute(sql);
        conn.close()
        return redirect(url_for('index'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # sss = request.args.get("str")
        # print(sss)
        # return 'post'
        user_id = request.form.get('username')
        # return user_id
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:

            curr_user = User()
            curr_user.id = user_id
            session['userid'] = user_id


            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user)
            flash('Wrong username or password!')
            # return redirect(url_for('login'))
            return 'Hi'+ user_id
            # return redirect(url_for('index'))
            # return 'Hi' + user_id
    #

    #
    # # GET 请求
    # return render_template('get')
    # return 'get'

    return redirect(url_for('login'))

@app.route("/", methods=['GET', 'POST'])
def home():
    # name = request.args.get("str")
    return '123'


@app.route("/index", methods=['GET', 'POST'])
# @login_required
# def index(username):
def index():
    # username = request.args.get("username")
    # print(username)
    if request.method == 'GET':
        # item = {
        #     "account_id": '123',
        #     "password": 'this is password',
        #     "username": '123'
        # }

        db = init_connection_engine()
        conn = db.connect()
        sql = 'select account_id, username, password from Account'
        query_results = conn.execute(sql).fetchall()
        conn.close()
        res = []
        for result in query_results:
            item = {
                "account_id": result[0],
                "username": result[1],
                "password": result[2]
            }
            res.append(item)
        return render_template("index.html", items=res)
        # return username
        # username = session.get('user_id')
        # # print(username)
        # if username is None:
        #     # return redirect(url_for('login'))
        #     return 'not exist'
        # else:
        #     return username


def init_connection_engine():
    # detect env local or gcp

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username='root',
            password='123123',
            database='db',
            host='35.223.202.39'
        )
    )

    return pool

if __name__ == "__main__":
    app.run()