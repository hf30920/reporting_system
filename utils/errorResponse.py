from flask import render_template

# 错误响应函数
def errorResponse(errorMsg):
    # 返回错误页面模板及错误信息
    return render_template('error.html',errorMsg=errorMsg)