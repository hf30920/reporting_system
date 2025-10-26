# Flask 完整教程

**Date: October 24, 2025**

**Author: Python 开发指南**

**Version: Flask 2.x**



***

## 目录



1. [教程介绍](#教程介绍)

2. [环境搭建](#环境搭建)

3. [第一个 Flask 应用](#第一个flask应用)

4. [路由和视图函数](#路由和视图函数)

5. [模板系统](#模板系统)

6. [表单处理](#表单处理)

7. [数据库集成](#数据库集成)

8. [项目结构最佳实践](#项目结构最佳实践)

9. [蓝图 Blueprint](#蓝图blueprint)

10. [用户认证](#用户认证)

11. [部署应用](#部署应用)

12. [总结和进阶学习](#总结和进阶学习)



***

## 教程介绍

Flask 是一个轻量级的 Python Web 框架，由 Armin Ronacher 创建。它被称为 "微框架"，因为它保持核心简单而灵活，但可以通过扩展来增加功能。

### Flask 的特点



* **轻量级**: 核心功能简洁，只包含 Web 开发的必需品

* **灵活**: 可以根据项目需求选择合适的扩展

* **易学**: 语法简单，容易上手

* **强大**: 支持复杂的 Web 应用开发

* **活跃的社区**: 丰富的扩展和文档

### 本教程将学习到



* Flask 基础概念和核心功能

* 路由设计和视图函数

* 模板系统和静态文件

* 表单处理和数据验证

* 数据库集成

* 项目结构最佳实践

* 用户认证和授权

* 应用部署



***

## 环境搭建

### 1. 安装 Python

确保你的系统安装了 Python 3.6 或更高版本：



```
python --version

\# 或

python3 --version
```

### 2. 创建虚拟环境

使用虚拟环境可以隔离项目依赖：



```
\# 创建项目目录

mkdir flask-tutorial

cd flask-tutorial

\# 创建虚拟环境

python -m venv venv

\# 激活虚拟环境

\# Windows

venv\\\Scripts\\\activate

\# macOS/Linux

source venv/bin/activate
```

### 3. 安装 Flask



```
pip install flask
```

验证安装：



```
python -c "import flask; print('Flask version:', flask.\_\_version\_\_)"
```



***

## 第一个 Flask 应用

### 创建基本应用

创建一个名为`app.py`的文件：



```
from flask import Flask

\# 创建Flask应用实例

app = Flask(\_\_name\_\_)

\# 定义路由和视图函数

@app.route('/')

def home():

     return '\<h1>Hello, Flask!\</h1>'

\# 启动应用

if \_\_name\_\_ == '\_\_main\_\_':

     app.run(debug=True)
```

### 运行应用



```
python app.py
```

访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 可以看到 "Hello, Flask!" 的输出。

### 代码解释



* `Flask(__name__)`: 创建 Flask 应用实例，`__name__`告诉 Flask 应用的根目录

* `@app.route('/')`: 路由装饰器，将 URL 路径映射到视图函数

* `home()`: 视图函数，处理请求并返回响应

* `app.run(debug=True)`: 启动开发服务器，`debug=True`开启调试模式



***

## 路由和视图函数

### 基础路由



```
from flask import Flask

app = Flask(\_\_name\_\_)

\# 根路由

@app.route('/')

def index():

     return 'Welcome to the homepage!'

\# 关于页面

@app.route('/about')

def about():

     return 'About us page'

\# 联系页面

@app.route('/contact')

def contact():

     return 'Contact information'
```

### 动态路由参数



```
\# 接收字符串参数

@app.route('/user/\<username>')

def user\_profile(username):

     return f'User Profile: {username}'

\# 接收整数参数

@app.route('/post/\<int:post\_id>')

def show\_post(post\_id):

     return f'Post ID: {post\_id}'

\# 接收浮点数参数

@app.route('/price/\<float:amount>')

def show\_price(amount):

     return f'Price: \${amount:.2f}'

\# 接收路径参数（包含斜杠）

@app.route('/path/\<path:subpath>')

def show\_subpath(subpath):

     return f'Subpath: {subpath}'
```

### HTTP 方法



```
from flask import request

\# 只接受GET方法（默认）

@app.route('/get-data', methods=\['GET'])

def get\_data():

     return 'This is a GET request'

\# 只接受POST方法

@app.route('/submit-data', methods=\['POST'])

def submit\_data():

     return 'This is a POST request'

\# 接受多种方法

@app.route('/api/data', methods=\['GET', 'POST', 'PUT', 'DELETE'])

def api\_data():

     if request.method == 'GET':

         return 'GET request received'

     elif request.method == 'POST':

         return 'POST request received'

     elif request.method == 'PUT':

         return 'PUT request received'

     elif request.method == 'DELETE':

         return 'DELETE request received'
```

### URL 构建



```
from flask import url\_for, redirect

@app.route('/')

def index():

     # 构建URL

     about\_url = url\_for('about')

     user\_url = url\_for('user\_profile', username='john')

     return '\<h1>Home\</h1>\<a href="' + about\_url + '">About\</a>\<br>\<a href="' + user\_url + '">John's Profile\</a>'

@app.route('/redirect-example')

def redirect\_example():

     \# 重定向到其他路由

     return redirect(url\_for('index'))
```



***

## 模板系统

Flask 使用 Jinja2 作为模板引擎，可以将 HTML 与 Python 代码分离。

### 创建模板目录



```
mkdir templates
```

### 基础模板使用

**templates/base.html**



```
\<!DOCTYPE html>

\<html lang="zh-CN">

\<head>

     \<meta charset="UTF-8">

     \<meta name="viewport" content="width=device-width, initial-scale=1.0">

     \<title>{% block title %}My Flask App{% endblock %}\</title>

     \<link rel="stylesheet" href="{{ url\_for('static', filename='css/style.css') }}">

\</head>

\<body>

     \<nav>

         \<a href="{{ url\_for('index') }}">Home\</a>

         \<a href="{{ url\_for('about') }}">About\</a>

         \<a href="{{ url\_for('contact') }}">Contact\</a>

     \</nav>

      

     \<div class="content">

         {% block content %}{% endblock %}

     \</div>

      

     \<footer>

         \&copy; 2025 My Flask App

     \</footer>

\</body>

\</html>
```

**templates/index.html**



```
{% extends "base.html" %}

{% block title %}Home - My Flask App{% endblock %}

{% block content %}

     \<h1>Welcome to the Homepage!\</h1>

      

     {% if username %}

         \<p>Hello, {{ username }}!\</p>

     {% else %}

         \<p>Please log in.\</p>

     {% endif %}

      

     \<h2>Latest Posts\</h2>

     \<ul>

         {% for post in posts %}

             \<li>

                 \<h3>{{ post.title }}\</h3>

                 \<p>{{ post.content }}\</p>

                 \<small>Published on: {{ post.date.strftime('%Y-%m-%d') }}\</small>

             \</li>

         {% endfor %}

     \</ul>

{% endblock %}
```

### 在视图函数中使用模板



```
from flask import render\_template

from datetime import datetime

@app.route('/')

def index():

     # 模拟数据

     posts = \[

         {

             'title': 'First Post',

             'content': 'This is the first post content.',

             'date': datetime(2025, 10, 20)

         },

         {

             'title': 'Second Post',

             'content': 'This is the second post content.',

             'date': datetime(2025, 10, 21)

         }

     ]

      

     return render\_template('index.html',  

                           username='Guest',  

                           posts=posts)
```

### 静态文件

创建静态文件目录：



```
mkdir -p static/css static/js static/images
```

**static/css/style.css**



```
body {

     font-family: Arial, sans-serif;

     line-height: 1.6;

     margin: 0;

     padding: 0;

     color: #333;

}

nav {

     background-color: #333;

     padding: 1rem;

}

nav a {

     color: white;

     margin-right: 1rem;

     text-decoration: none;

}

.content {

     padding: 2rem;

}

footer {

     background-color: #f4f4f4;

     text-align: center;

     padding: 1rem;

     position: fixed;

     bottom: 0;

     width: 100%;

}
```



***

## 表单处理

### 基本表单处理

**templates/contact.html**



```
{% extends "base.html" %}

{% block title %}Contact - My Flask App{% endblock %}

{% block content %}

     \<h1>Contact Us\</h1>

      

     {% if success %}

         \<div class="success">Message sent successfully!\</div>

     {% endif %}

      

     \<form method="POST" action="{{ url\_for('contact') }}">

         \<div>

             \<label for="name">Name:\</label>

             \<input type="text" id="name" name="name" required>

         \</div>

          

         \<div>

             \<label for="email">Email:\</label>

             \<input type="email" id="email" name="email" required>

         \</div>

          

         \<div>

             \<label for="message">Message:\</label>

             \<textarea id="message" name="message" required>\</textarea>

         \</div>

          

         \<button type="submit">Send Message\</button>

     \</form>

{% endblock %}
```



```
from flask import request, flash

@app.route('/contact', methods=\['GET', 'POST'])

def contact():

     if request.method == 'POST':

         # 获取表单数据

         name = request.form.get('name')

         email = request.form.get('email')

         message = request.form.get('message')

          

         # 处理表单数据（这里只是简单打印）

         print(f"New message from {name} ({email}): {message}")

          

         # 可以添加数据验证、发送邮件等逻辑

          

         return render\_template('contact.html', success=True)

      

     return render\_template('contact.html', success=False)
```

### 使用 Flask-WTF 处理表单

安装 Flask-WTF：



```
pip install flask-wtf
```

**app.py**



```
from flask\_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField

from wtforms.validators import DataRequired, Email

\# 创建表单类

class ContactForm(FlaskForm):

     name = StringField('Name', validators=\[DataRequired()])

     email = StringField('Email', validators=\[DataRequired(), Email()])

     message = TextAreaField('Message', validators=\[DataRequired()])

     submit = SubmitField('Send Message')

@app.route('/contact-wtf', methods=\['GET', 'POST'])

def contact\_wtf():

     form = ContactForm()

      

     if form.validate\_on\_submit():

         # 表单验证成功

         name = form.name.data

         email = form.email.data

         message = form.message.data

          

         print(f"New message from {name} ({email}): {message}")

          

         # 可以添加flash消息

         flash('Message sent successfully!', 'success')

          

         return redirect(url\_for('contact\_wtf'))

      

     return render\_template('contact\_wtf.html', form=form)
```



***

## 数据库集成

### 使用 Flask-SQLAlchemy

安装 Flask-SQLAlchemy：



```
pip install flask-sqlalchemy
```

### 配置数据库



```
from flask\_sqlalchemy import SQLAlchemy

import os

app = Flask(\_\_name\_\_)

\# 配置数据库

basedir = os.path.abspath(os.path.dirname(\_\_file\_\_))

app.config\['SQLALCHEMY\_DATABASE\_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

app.config\['SQLALCHEMY\_TRACK\_MODIFICATIONS'] = False

app.config\['SECRET\_KEY'] = 'your-secret-key-here'  # 用于表单CSRF保护

\# 初始化数据库

db = SQLAlchemy(app)
```

### 定义数据模型



```
from datetime import datetime

class User(db.Model):

     id = db.Column(db.Integer, primary\_key=True)

     username = db.Column(db.String(80), unique=True, nullable=False)

     email = db.Column(db.String(120), unique=True, nullable=False)

     password\_hash = db.Column(db.String(128))

     posts = db.relationship('Post', backref='author', lazy=True)

     created\_at = db.Column(db.DateTime, default=datetime.utcnow)

     def \_\_repr\_\_(self):

         return f'\<User {self.username}>'

class Post(db.Model):

     id = db.Column(db.Integer, primary\_key=True)

     title = db.Column(db.String(100), nullable=False)

     content = db.Column(db.Text, nullable=False)

     created\_at = db.Column(db.DateTime, default=datetime.utcnow)

     updated\_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     user\_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     def \_\_repr\_\_(self):

         return f'\<Post {self.title}>'
```



***

## 项目结构最佳实践

对于中大型 Flask 应用，良好的项目结构非常重要。

### 推荐的项目结构



```
flask-tutorial/

│

├── app/                        # 主应用包

│   ├── \_\_init\_\_.py             # 应用工厂

│   ├── models/                 # 数据模型

│   │   ├── \_\_init\_\_.py

│   │   ├── user.py

│   │   └── post.py

│   │

│   ├── routes/                 # 路由和视图

│   │   ├── \_\_init\_\_.py

│   │   ├── main.py             # 主要路由

│   │   ├── auth.py             # 认证路由

│   │   └── blog.py             # 博客路由

│   │

│   ├── forms/                  # 表单类

│   │   ├── \_\_init\_\_.py

│   │   ├── auth.py

│   │   └── blog.py

│   │

│   ├── templates/              # HTML模板

│   │   ├── base.html

│   │   ├── auth/

│   │   │   ├── login.html

│   │   │   └── register.html

│   │   └── blog/

│   │       ├── index.html

│   │       ├── post.html

│   │       └── create.html

│   │

│   ├── static/                 # 静态文件

│   │   ├── css/

│   │   │   └── style.css

│   │   ├── js/

│   │   │   └── main.js

│   │   └── images/

│   │

│   └── utils/                  # 工具函数

│       ├── \_\_init\_\_.py

│       ├── auth.py

│       └── helpers.py

│

├── config.py                   # 配置文件

├── run.py                      # 应用入口

├── requirements.txt            # 项目依赖

├── migrations/                 # 数据库迁移文件

└── tests/                      # 测试文件

     ├── \_\_init\_\_.py

     ├── test\_auth.py

     └── test\_blog.py
```

### 应用工厂模式

**app/****init.py**



```
from flask import Flask

from flask\_sqlalchemy import SQLAlchemy

from flask\_wtf.csrf import CSRFProtect

from config import Config

\# 初始化扩展

db = SQLAlchemy()

csrf = CSRFProtect()

def create\_app(config\_class=Config):

     """应用工厂函数"""

     app = Flask(\_\_name\_\_)

     app.config.from\_object(config\_class)

      

     # 初始化扩展

     db.init\_app(app)

     csrf.init\_app(app)

      

     # 注册蓝图

     from app.routes.main import bp as main\_bp

     from app.routes.auth import bp as auth\_bp

     from app.routes.blog import bp as blog\_bp

      

     app.register\_blueprint(main\_bp)

     app.register\_blueprint(auth\_bp, url\_prefix='/auth')

     app.register\_blueprint(blog\_bp, url\_prefix='/blog')

      

     # 创建数据库表

     with app.app\_context():

         db.create\_all()

      

     return app
```



***

## 蓝图 Blueprint

蓝图是 Flask 中组织大型应用的重要工具，它可以将应用分解为多个模块。

### 创建蓝图

**app/routes/****auth.py**



```
from flask import Blueprint, render\_template, redirect, url\_for, flash, request

from flask\_login import login\_user, logout\_user, login\_required, current\_user

from werkzeug.security import generate\_password\_hash, check\_password\_hash

from app import db

from app.models.user import User

from app.forms.auth import LoginForm, RegistrationForm

bp = Blueprint('auth', \_\_name\_\_)

@bp.route('/register', methods=\['GET', 'POST'])

def register():

     if current\_user.is\_authenticated:

         return redirect(url\_for('main.index'))

      

     form = RegistrationForm()

     if form.validate\_on\_submit():

         # 检查用户名和邮箱是否已存在

         if User.query.filter\_by(username=form.username.data).first():

             flash('Username already exists', 'danger')

             return redirect(url\_for('auth.register'))

          

         if User.query.filter\_by(email=form.email.data).first():

             flash('Email already exists', 'danger')

             return redirect(url\_for('auth.register'))

          

         # 创建新用户

         user = User(

             username=form.username.data,

             email=form.email.data,

             password\_hash=generate\_password\_hash(form.password.data)

         )

          

         db.session.add(user)

         db.session.commit()

          

         flash('Registration successful! You can now log in.', 'success')

         return redirect(url\_for('auth.login'))

      

     return render\_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=\['GET', 'POST'])

def login():

     if current\_user.is\_authenticated:

         return redirect(url\_for('main.index'))

      

     form = LoginForm()

     if form.validate\_on\_submit():

         user = User.query.filter\_by(username=form.username.data).first()

          

         if user and check\_password\_hash(user.password\_hash, form.password.data):

             login\_user(user, remember=form.remember\_me.data)

              

             # 处理记住的URL

             next\_page = request.args.get('next')

             if not next\_page or url\_parse(next\_page).netloc != '':

                 next\_page = url\_for('main.index')

              

             return redirect(next\_page)

         else:

             flash('Invalid username or password', 'danger')

      

     return render\_template('auth/login.html', title='Login', form=form)
```



***

## 用户认证

使用 Flask-Login 处理用户认证。

### 安装和配置 Flask-Login



```
pip install flask-login
```

**app/models/****user.py**



```
from flask\_login import UserMixin

from werkzeug.security import generate\_password\_hash, check\_password\_hash

from datetime import datetime

from app import db

class User(UserMixin, db.Model):

     id = db.Column(db.Integer, primary\_key=True)

     username = db.Column(db.String(80), unique=True, nullable=False)

     email = db.Column(db.String(120), unique=True, nullable=False)

     password\_hash = db.Column(db.String(128))

     posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')

     created\_at = db.Column(db.DateTime, default=datetime.utcnow)

      

     def set\_password(self, password):

         """设置密码哈希"""

         self.password\_hash = generate\_password\_hash(password)

      

     def check\_password(self, password):

         """验证密码"""

         return check\_password\_hash(self.password\_hash, password)

      

     def \_\_repr\_\_(self):

         return f'\<User {self.username}>'
```



***

## 部署应用

### 使用 Gunicorn 作为 WSGI 服务器

安装 Gunicorn：



```
pip install gunicorn
```

创建启动脚本 **wsgi.py**：



```
from app import create\_app

app = create\_app('production')

if \_\_name\_\_ == '\_\_main\_\_':

     app.run()
```

启动应用：



```
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

### 使用 Docker 部署

**Dockerfile**：



```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK\_APP=run.py

ENV FLASK\_ENV=production

ENV SECRET\_KEY=your-secret-key

EXPOSE 5000

CMD \["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```



***

## 总结和进阶学习

### 本教程总结

通过本教程，你已经学习了 Flask 的核心概念和实际应用：



1. **基础概念**: Flask 应用结构、路由、视图函数

2. **模板系统**: Jinja2 模板、模板继承、静态文件

3. **表单处理**: 基础表单、Flask-WTF 表单验证

4. **数据库集成**: SQLAlchemy ORM、数据模型、数据库操作

5. **项目结构**: 模块化设计、应用工厂模式

6. **蓝图**: 大型应用的模块化组织

7. **用户认证**: Flask-Login、用户管理

8. **部署**: 多种部署方式

### 进阶学习方向



1. **API 开发**

* 使用 Flask-RESTful 或 Flask-RESTX

* JWT 认证

* API 文档生成

1. **高级功能**

* Flask-SocketIO 实现实时通信

* Celery 处理异步任务

* Redis 缓存

* Elasticsearch 搜索引擎

1. **安全性**

* CSRF 保护

* XSS 防护

* SQL 注入防护

* 密码策略

1. **测试**

* 单元测试和集成测试

* pytest-flask

* 测试覆盖率

1. **性能优化**

* 数据库优化

* 缓存策略

* 负载均衡

### 推荐资源



1. **官方文档**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)

2. **扩展库文档**:

* Flask-SQLAlchemy: [https://flask-sqlalchemy.palletsprojects.com/](https://flask-sqlalchemy.palletsprojects.com/)

* Flask-WTF: [https://flask-wtf.readthedocs.io/](https://flask-wtf.readthedocs.io/)

* Flask-Login: [https://flask-login.readthedocs.io/](https://flask-login.readthedocs.io/)

1. **书籍推荐**:

* "Flask Web Development" by Miguel Grinberg

* "Learning Flask Framework" by Matt Copperwaite

### 实践建议



1. **从小项目开始**: 先构建简单的应用，逐步增加功能

2. **遵循最佳实践**: 保持良好的代码结构和设计模式

3. **持续学习**: Flask 生态系统一直在发展，关注最新动态

4. **参与社区**: 在 Stack Overflow、GitHub 等平台分享和学习

Flask 是一个非常强大而灵活的 Web 框架，掌握它将为你的 Python Web 开发之路打下坚实的基础。祝你学习愉快！



***

**版权声明**: 本教程采用 MIT 许可证，欢迎分享和修改。

**最后更新**: 2025 年 10 月 24 日

> （注：文档部分内容可能由 AI 生成）