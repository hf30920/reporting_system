from pymysql import *

# 建立数据库连接
conn = connect(host='localhost',user='root',password='root',database='wb',port=3306)
# 创建游标对象
cursor = conn.cursor()


# 数据库查询函数
def querys(sql,params,type='no_select'):
    # 将参数转为元组
    params = tuple(params)
    # 执行SQL语句
    cursor.execute(sql,params)
    # 检测连接是否有效，无效则重新连接
    conn.ping(reconnect=True)
    # 如果不是非查询操作，则获取查询结果
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        # 提交事务
        conn.commit()
        return '数据库语句执行成功'