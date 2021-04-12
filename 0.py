from flask import Flask, request, url_for, redirect, session, render_template
import pymysql
import todolist_sql


app = Flask(__name__)
app.secret_key = "secret_key"

mylist = todolist_sql.todolist()

@app.route('/')
def show_():
    return render_template('pages/0.html')


@app.route('/', methods=['POST'])  # 首页
def goto_login():
    return redirect("/login")


@app.route('/login', methods=['GET'])  # 登陆
def show_login():
    return render_template('pages/login.html')


@app.route('/login', methods=['POST'])  # 登陆
def goto_web():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return redirect("/web")
    else:
        return '<h3>输错了，憨憨（或者你只是想测试一下输错时的反应）</h3>'


@app.route('/web', methods=['GET', 'POST'])
def show_web():
    if request.method == 'GET':  # 渲染模版
        return render_template('pages/web.html')
    if request.method == 'POST':
        db = pymysql.connect(host='localhost', user='root', password='hlsfsysybj2.', port=3306, db='spiders')
        cursor = db.cursor()
        sql_create = 'CREATE TABLE IF NOT EXISTS todolist (title VARCHAR(255) NOT NULL, type VARCHAR(255) NOT NULL, ' \
                     'content VARCHAR(2555) NOT NULL, startline VARCHAR(255) NOT NULL, deadline VARCHAR(255) NOT ' \
                     'NULL, tips VARCHAR(2555) NOT NULL, completion VARCHAR(2555) NOT NULL, PRIMARY KEY (title)) '
        cursor.execute(sql_create)
        sql_insert = 'INSERT INTO todolist(title, type, content, startline, deadline, tips, completion) values(%s, %s, %s, %s, %s, %s, %s)'
        add_title = request.form['title']
        add_type = request.form['type']
        add_content = request.form['content']
        add_startline = request.form['startline']
        add_deadline = request.form['deadline']
        add_tips = request.form['tips']
        add_completion = request.form['completion']
        cursor.execute(sql_insert, (add_title, add_type, add_content, add_startline, add_deadline, add_tips, add_completion))
        db.commit()
        db.close()
        return {
            "title": add_title,
            "type": add_type,
            "content": add_content,
            "startline": add_startline,
            "deadline": add_deadline,
            "tips": add_tips,
            "completion": add_completion,
        }

@app.route('/weblist')
def show_weblist():
    mylist.todolist_select()


if __name__ == "__main__":
    app.run()
