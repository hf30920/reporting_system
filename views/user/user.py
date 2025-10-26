from flask import Flask,session,render_template,redirect,Blueprint,request
from utils.errorResponse import *
import time
from utils.query import querys
# 创建用户蓝图
ub = Blueprint('user',__name__,url_prefix='/user',template_folder='templates')

# 登录路由，支持GET和POST方法
@ub.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # 将表单数据转为字典
        request.form = dict(request.form)

        # 过滤函数，检查用户名和密码是否匹配
        def filter_fns(item):
            return request.form['username'] in item and request.form['password'] in item

        # 查询所有用户信息
        users = querys('select * from user', [], 'select')
        # 筛选登录成功的用户
        login_success = list(filter(filter_fns, users))
        # 如果没有匹配的用户，返回错误信息
        if not len(login_success):
            return errorResponse('输入的密码或账号出现问题')

        # 将用户名存入会话
        session['username'] = request.form['username']
        session['createTime'] = login_success[0][-1]
        # 登录成功后跳转到主页
        return redirect('/page/home', 301)
    else:
        # GET请求返回登录页面
        return render_template('login.html')



# 注册路由，支持GET和POST方法
@ub.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # 将表单数据转为字典
        request.form = dict(request.form)
        # 检查两次输入的密码是否一致
        if request.form['password'] != request.form['passwordCheked']:
            return '两次密码不符'
        else:
            # 过滤函数，检查用户名是否已存在
            def filter_fn(item):
                return request.form['username'] in item

            # 查询所有用户信息
            users = querys('select * from user', [], 'select')
            # 筛选已存在的用户名
            filter_list = list(filter(filter_fn, users))
            # 如果用户名已存在，返回错误信息
            if len(filter_list):
                return errorResponse('该用户名已被注册')
            else:
                # 获取当前时间
                time_tuple = time.localtime(time.time())
                # 插入新用户信息到数据库
                querys('insert into user(username,password,createTime) values(%s,%s,%s)',
                       [request.form['username'], request.form['password'],
                        str(time_tuple[0]) + '-' + str(time_tuple[1]) + '-' + str(time_tuple[2])])

        # 注册成功后跳转到登录页面
        return redirect('/user/login', 301)

    else:
        # GET请求返回注册页面
        return render_template('register.html')

# 用户登出路由
@ub.route('/logOut',methods=['GET','POST'])
def logOut():
    # 清除会话信息
    session.clear()
    # 跳转到登录页面
    return redirect('/user/login')