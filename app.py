from flask import Flask,session,render_template,redirect,request
import re
# 创建Flask应用实例
app = Flask(__name__)
# 设置应用密钥用于会话加密
app.secret_key = 'This is a app.secret_Key , You Know ?'

# 导入蓝图模块
from views.page import page
from views.user import user
# 注册蓝图
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

# 根路由，重定向到登录页面
@app.route('/')
def index():
    return redirect('/user/login')

# 请求前钩子，用于权限验证
@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    # 如果请求的是静态资源，则放行
    if re.search(pat,request.path):
        return
    # 允许访问登录和注册页面
    if request.path == '/user/login':
        return
    if request.path == '/user/register':
        return
    # 检查用户是否已登录
    uname = session.get('username')
    if uname:
        return None

    # 未登录则重定向到登录页面
    return redirect('/user/login')

# 处理404错误页面
@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')

# 应用启动入口
if __name__ == '__main__':
    app.run()
