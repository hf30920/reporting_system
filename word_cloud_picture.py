import jieba  # 分词
from matplotlib import pylab as plt     # 绘图，数据可视化
from wordcloud import WordCloud         # 词云
from PIL import Image                   # 图片处理
import numpy as np                      # 矩阵运算
from pymysql import *
import json
# wordCloud

# 生成词云图片函数
def get_img(field,targetImgSrc,resImgSrc):
    # 建立数据库连接
    con = connect(host='localhost', user='root', password='root', database='heischool', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    # 查询指定字段的数据
    sql = f"select {field} from article"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    # 拼接所有文本内容
    for item in data:
        text = text + item[0]
    cursor.close()
    con.close()

    # 分词处理
    cut = jieba.cut(text)
    string = ' '.join(cut)
    print(string)

    # 图片处理
    img = Image.open(targetImgSrc)  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为数组
    # 创建词云对象
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    # 生成词云
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 保存词云图片到文件
    plt.savefig(resImgSrc, dpi=500)

get_img('content',r'.\static\3.jpg',r'.\static\content_cloud.jpg')
# get_img('summary',r'.\static\2.jpg',r'.\static\summary_cloud.jpg')
# get_img('casts',r'.\static\content.jpg',r'.\static\casts_cloud.jpg')

