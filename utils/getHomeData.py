# 导入所需的模块
from utils import getPublicData
from datetime import datetime
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import jieba

# 获取首页点赞数最高的前几条评论数据
def getHomeTopLikeCommentsData():
    # 获取所有评论数据
    commentsList = getPublicData.getAllCommentsData()
    # 按照评论的点赞数(索引为2的字段)进行降序排序，并取前4条数据
    commentsListSorted = list(sorted(commentsList,key=lambda x:int(x[2]),reverse=True))[:4]
    return commentsListSorted

# 获取首页标签数据（文章总数、最多点赞数的作者名、文章数最多的城市）
def getTagData():
    # 获取所有文章数据
    articleData = getPublicData.getAllData()
    maxLikeNum = 0          # 最大点赞数
    maxLikeAuthorName = ''  # 最大点赞数对应的作者名
    cityDic = {}            # 城市字典，用于统计各城市的文章数量
    
    # 遍历所有文章数据
    for article in articleData:
        # 查找点赞数最多的文章及其作者
        if int(article[1]) > maxLikeNum:
            maxLikeNum = int(article[1])
            maxLikeAuthorName = article[11]  # 作者名在索引为11的位置
        
        # 跳过没有城市信息的文章
        if article[4] == '无':
            continue
            
        # 统计各城市的文章数量
        if cityDic.get(article[4],-1) == -1:
            cityDic[article[4]] = 1
        else:
            cityDic[article[4]] += 1
    
    # 找出文章数最多的城市
    maxCity = list(sorted(cityDic.items(),key=lambda x:x[1],reverse=True))[0][0]

    # 返回文章总数、最多点赞数的作者名、文章数最多的城市
    return len(articleData),maxLikeAuthorName,maxCity

# 获取文章创建数量的图表数据（用于ECharts展示）
def getCreatedNumEchartsData():
    # 获取所有文章数据
    articleData = getPublicData.getAllData()
    
    # 提取所有唯一的创建日期，并去重
    xData = list(set([x[7] for x in articleData]))
    
    # 按日期时间戳进行排序，最新的日期在前
    xData = list(sorted(xData,key=lambda x:datetime.strptime(x,'%Y-%m-%d').timestamp(),reverse=True))
    
    # 初始化y轴数据，每个日期对应的文章数初始为0
    yData = [0 for x in range(len(xData))]
    
    # 统计每天的文章数量
    for i in articleData:
        for index,j in enumerate(xData):
            if i[7] == j:  # 如果文章创建日期与x轴日期匹配
                yData[index] += 1  # 对应日期的文章数加1

    return xData,yData

# 获取文章类型分布的图表数据
def getTypeCharData():
    # 获取所有文章数据
    allData = getPublicData.getAllData()
    typeDic = {}  # 类型字典，用于统计各类型文章数量
    
    # 遍历所有文章，统计各类型文章数量
    for i in allData:
        if typeDic.get(i[8], -1) == -1:  # 类型信息在索引为8的位置
            typeDic[i[8]] = 1
        else:
            typeDic[i[8]] += 1
    
    # 构造结果数据格式，用于ECharts饼图展示
    resultData = []
    for key, value in typeDic.items():
        resultData.append({
            'name': key,    # 类型名称
            'value': value, # 该类型文章数量
        })
    return resultData

# 获取评论用户创建数量的图表数据
def getCommentsUserCratedNumEchartsData():
    # 获取所有评论数据
    userData = getPublicData.getAllCommentsData()
    createdDic = {}  # 用户字典，用于统计各用户评论数量
    
    # 遍历所有评论，统计各用户评论数量
    for i in userData:
        if createdDic.get(i[1],-1) == -1:  # 用户名在索引为1的位置
            createdDic[i[1]] =1
        else:
            createdDic[i[1]] +=1
    
    # 构造结果数据格式，用于ECharts展示
    resultData = []
    for key,value in createdDic.items():
        resultData.append({
            'name':key,     # 用户名
            'value':value,  # 该用户评论数量
        })
    return resultData

# 加载停用词列表
def stopwordslist():
    # 从文件中读取停用词，每行一个停用词，去除首尾空白字符
    stopwords = [line.strip() for line in open('./model/stopWords.txt',encoding='UTF-8').readlines()]
    return stopwords

# 生成用户名词云图片
def getUserNameWordCloud():
    text = ''  # 存储所有用户名的文本
    stopwords = stopwordslist()  # 获取停用词列表
    commentsList = getPublicData.getAllCommentsData()  # 获取所有评论数据
    
    # 拼接所有评论中的用户名（索引为5的位置）
    for comment in commentsList:
        text += comment[5]
    
    # 对文本进行分词处理
    cut = jieba.cut(text)
    newCut = []
    
    # 过滤掉停用词
    for word in cut:
        if word not in stopwords:
            newCut.append(word)
    
    # 将分词结果用空格连接成字符串
    string = ' '.join(newCut)
    
    # 创建词云对象并设置相关参数
    wc = WordCloud(
        width=1000,              # 词云图片宽度
        height=600,              # 词云图片高度
        background_color='white', # 背景颜色
        colormap='Blues',        # 颜色映射
        font_path='STHUPO.TTF'   # 字体路径
    )
    
    # 根据文本生成词云
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 显示生成的词语图片
    # plt.show()

    # 保存词云图片到文件
    plt.savefig('./static/authorNameCloud.jpg', dpi=500)