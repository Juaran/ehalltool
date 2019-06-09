import importlib
import sys
importlib.reload(sys)
import os
import pymysql
import pymysql.cursors
import time
import warnings
warnings.filterwarnings("ignore")

from flask import *

from preLogin import loginResult
from showData import show
from ehallTool.aiutil import airoot

from config import *


app = Flask(__name__)
app.secret_key = os.urandom(24)

username = '20161040170'

@app.route('/')
def prelogin():
    return redirect(url_for("login"))  # 重定向到登录

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # get 登录界面
        return render_template("login.html")

    if request.method == "POST":  # 在登录界面提交表单
        global username

        username = request.form.get("username")  # 获取username
        password = request.form.get("password")  # 获取password

        """ 登录校验 """
        if username != '' and password != '' and username.isdigit() and len(username)==11:
            login_result = loginResult.get_result(username, password)

            if login_result:
                # 登录成功
                flash("登录成功！")
                return redirect(url_for("index", username=username))  # 登录成功跳转首页

            else:
                # 登录失败
                flash("登录失败！")  # 页面显示闪现消息
                return render_template("login.html")
        else:
            flash("登录失败！")  # 页面显示闪现消息
            return render_template("login.html")


@app.route('/index/')
def index():
    username = request.args.get("username")

    return render_template("index.html", username=username)


@app.route('/ai_root/', methods=['GET', 'POST'])
def ai_root():
    if request.method == 'POST':
        word = request.form.get('word')
        # 这里调用对象的方法
        res = airoot().getword(word)
        return render_template('ai_root.html', res=res)
    else:
        return render_template('ai_root.html', res='')



@app.route('/welcome/')
def welcome():
    username = request.args.get("username")
    return render_template("welcome.html", username=username)


# 初始化学期，默认显示入学第一学期信息
term = str(int(username) - 1) + '-' + username[:4] + "-2"


@app.route('/index/<username>/course/', methods=['POST', 'GET'])
def course(username):

    global term

    if request.method == 'GET':
        courses = show.Show(username).course(term)

        if courses is not None:
            return render_template("course.html", courses=courses, term=int(username[:4]), username=username)
        else:
            term = "2017-2018-1"
            return render_template("nothing.html")

    if request.method == 'POST':
        chooseTerm = request.get_data().decode("utf-8")

        year = chooseTerm[:4]
        season = "1"
        if chooseTerm[5] == "秋":
            season = "2"

        term = str(int(year)-1) + "-" + year + "-" + season
        print(term)
        return "选取学期", term


@app.route('/index/<username>/grades/', methods=['POST', 'GET'])
def grades(username):

    global term

    if request.method == "GET":
        grades = show.Show(username).grades(term)
        if grades is not None:
            return render_template("grades.html", grades=grades, term=int(username[:4]), username=username)
        else:
            term = "2017-2018-1"
            return render_template("nothing.html")

    if request.method == 'POST':
        chooseTerm = request.get_data().decode("utf-8")

        year = chooseTerm[:4]
        season = "1"
        if chooseTerm[5] == "秋":
            season = "2"

        term = str(int(year) - 1) + "-" + year + "-" + season
        print(term)
        return "选取学期", term


@app.route('/index/<username>/exams/', methods=['POST', 'GET'])
def exams(username):
    global term

    if request.method == "GET":
        exams = show.Show(username).exam(term)
        if exams is not None:
            return render_template("exams.html", exams=exams, term=int(username[:4]), username=username)
        else:
            term = "2017-2018-1"
            return render_template("nothing.html")

    if request.method == 'POST':
        chooseTerm = request.get_data().decode("utf-8")

        year = chooseTerm[:4]
        season = "1"
        if chooseTerm[5] == "秋":
            season = "2"

        term = str(int(year) - 1) + "-" + year + "-" + season
        print(term)
        return "选取学期", term


# 增加

# 连接数据库
def connectdb():
    db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE, charset='utf8')
    cursor = db.cursor()
    db.autocommit(True)

    return (db, cursor)

def createdb():
    (db, cursor) = connectdb()

    """ 创建表 """
    sql = """CREATE TABLE IF NOT EXISTS `Blog` (
                  `id` int(20) NOT NULL AUTO_INCREMENT,
                  `title` char(100) NOT NULL ,
                  `content` varchar(16383) DEFAULT NULL,
                  `timestamp` char(255) DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8; """
    cursor.execute(sql)

# 关闭数据库
def closedb(db,cursor):
    db.close()
    cursor.close()


# 首页 /index/<username>/exams/
@app.route('/blog/')
def blog():
    createdb()
    return render_template('blog.html')


# 处理表单提交
@app.route('/handle', methods=['POST'])
def handle():
    # 获取post数据
    data = request.form

    # 连接数据库
    (db,cursor) = connectdb()

    # 添加数据
    cursor.execute("INSERT INTO Blog(title, content, timestamp) VALUES(%s, %s, %s)",
                   [data['title'] + " 作者："+ username, data['content'], str(int(time.time()))])

    # 最后添加行的id
    post_id = cursor.lastrowid

    # 关闭数据库
    closedb(db,cursor)

    return redirect(url_for('post', post_id=post_id))

# 文章列表页
@app.route('/list')
def listb():
    # 连接数据库
    (db,cursor) = connectdb()

    # 获取数据
    cursor.execute("SELECT * FROM Blog")
    posts = cursor.fetchall()

    # 格式化时间戳
    new_posts = []
    for post in posts:
        post = list(post)
        post[-1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(post[-1])))

        new_posts.append(list(post))

    # 关闭数据库
    closedb(db,cursor)

    # 后端向前端传递数据
    return render_template('list.html', posts=new_posts)


# 文章详情页
@app.route('/post/<post_id>')
def post(post_id):
    # 连接数据库
    (db,cursor) = connectdb()

    # 查询数据
    cursor.execute("SELECT * FROM Blog WHERE id = %s", [post_id])
    post = cursor.fetchone()

    # 格式化时间戳
    post = list(post)
    post[-1] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(post[-1])))

    # 关闭数据库
    closedb(db,cursor)

    # 后端向前端传递数据
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(host=WEB_HOST, port=WEB_PORT, debug=DEBUG)
