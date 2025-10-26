from utils import getPublicData
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image                   # 图片处理
import numpy as np
from snownlp import SnowNLP

# 获取文章类型列表
def getTypeList():
    typeList = list(set([x[8] for x in getPublicData.getAllData()]))
    return typeList

# 获取文章图表一数据（点赞数分布）
def getArticleCharOneData(defaultType):
    articleList = getPublicData.getAllData()
    xData = []
    rangeNum = 1000
    # 构造点赞数区间
    for item in range(1,15):
        xData.append(str(rangeNum * item)+ '-' + str(rangeNum*(item+1)))
    # 初始化各区间的数量为0
    yData = [0 for x in range(len(xData))]
    # 统计各区间内的文章数量
    for article in articleList:
        if article[8] != defaultType:
            for item in range(14):
                if int(article[1]) < rangeNum*(item+2):
                    yData[item] += 1
                    break
    return xData,yData

# 获取文章图表二数据（评论数分布）
def getArticleCharTwoData(defaultType):
    articleList = getPublicData.getAllData()
    xData = []
    rangeNum = 1000
    # 构造评论数区间
    for item in range(1,15):
        xData.append(str(rangeNum * item)+ '-' + str(rangeNum*(item+1)))
    # 初始化各区间的数量为0
    yData = [0 for x in range(len(xData))]
    # 统计各区间内的文章数量
    for article in articleList:
        if article[8] != defaultType:
            for item in range(14):
                if int(article[2]) < rangeNum*(item+2):
                    yData[item] += 1
                    break
    return xData,yData

# 获取文章图表三数据（转发数分布）
def getArticleCharThreeData(defaultType):
    articleList = getPublicData.getAllData()
    xData = []
    rangeNum = 50
    # 构造转发数区间
    for item in range(1, 30):
        xData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    # 初始化各区间的数量为0
    yData = [0 for x in range(len(xData))]
    # 统计各区间内的文章数量
    for article in articleList:
        if article[8] != defaultType:
            for item in range(29):
                if int(article[2]) < rangeNum * (item + 2):
                    yData[item] += 1
                    break
    return xData, yData

# 获取地理位置图表数据（评论）
def getGeoCharDataTwo():
    cityList = getPublicData.cityList
    commentList = getPublicData.getAllCommentsData()
    cityDic = {}
    # 统计各省份评论数量
    for comment in commentList:
        if comment[3] == '无': continue
        for j in cityList:
            if j['province'].find(comment[3]) != -1:
                if cityDic.get(j['province'], -1) == -1:
                    cityDic[j['province']] = 1
                else:
                    cityDic[j['province']] += 1

    # 构造结果数据
    cityDicList = []
    for key, value in cityDic.items():
        cityDicList.append({
            'name': key,
            'value': value
        })
    return cityDicList


# 获取地理位置图表数据（文章）
def getGeoCharDataOne():
    cityList = getPublicData.cityList
    articleList = getPublicData.getAllData()

    cityDic = {}
    # 统计各省份文章数量
    for article in articleList:
        if article[4] == '无':continue
        for j in cityList:
                if j['province'].find(article[4]) != -1:
                    if cityDic.get(j['province'],-1) == -1:
                        cityDic[j['province']] = 1
                    else:
                        cityDic[j['province']] += 1

    # 构造结果数据
    cityDicList = []
    for key, value in cityDic.items():
        cityDicList.append({
            'name': key,
            'value': value
        })
    return cityDicList

# 获取评论图表一数据（点赞数分布）
def getCommetCharDataOne():
    commentList = getPublicData.getAllCommentsData()
    xData = []
    rangeNum = 20
    # 构造点赞数区间
    for item in range(1, 100):
        xData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    # 初始化各区间的数量为0
    yData = [0 for x in range(len(xData))]
    # 统计各区间内的评论数量
    for comment in commentList:
            for item in range(99):
                if int(comment[2]) < rangeNum * (item + 2):
                    yData[item] += 1
                    break
    return xData, yData

# 获取评论图表二数据（性别分布）
def getCommetCharDataTwo():
    commentList = getPublicData.getAllCommentsData()
    # 性别字典，用于统计各性别评论数量
    genderDic = {}
    # 统计各性别评论数量
    for i in commentList:
        if genderDic.get(i[6],-1) == -1:
            genderDic[i[6]] = 1
        else:
            genderDic[i[6]] += 1
    # 构造结果数据
    resultData = [{
        'name':x[0],
        'value':x[1]
    } for x in genderDic.items()]
    return resultData

# 加载停用词列表
def stopwordslist():
    # 读取停用词文件，去除每行首尾空白字符
    stopwords = [line.strip() for line in open('./model/stopWords.txt',encoding='UTF-8').readlines()]
    return stopwords

# 生成内容词云
def getContentCloud():
    text = ''
    # 获取停用词列表
    stopwords = stopwordslist()
    # 获取所有文章数据
    articleList = getPublicData.getAllData()
    # 拼接所有文章内容
    for article in articleList:
        text += article[5]
    # 分词处理
    cut = jieba.cut(text)
    newCut = []
    # 去除停用词
    for word in cut:
        if word not in stopwords: newCut.append(word)
    string = ' '.join(newCut)
    # 打开遮罩图片
    img = Image.open('./static/content.jpg')  
    img_arr = np.array(img)  # 将图片转化为数组
    # 创建词云对象
    wc = WordCloud(
        width=1000, height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',
        mask=img_arr,
    )
    # 生成词云
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 保存词云图片到文件
    plt.savefig('./static/contentCloud.jpg', dpi=500)

# 生成评论词云
def getCommentContentCloud():
    text = ''
    # 获取停用词列表
    stopwords = stopwordslist()
    # 获取所有评论数据
    commentsList = getPublicData.getAllCommentsData()
    # 拼接所有评论内容
    for comment in commentsList:
        text += comment[4]
    # 分词处理
    cut = jieba.cut(text)
    newCut = []
    # 去除停用词
    for word in cut:
        if word not in stopwords:newCut.append(word)
    string = ' '.join(newCut)
    # 打开遮罩图片
    img = Image.open('./static/comment.jpg') 
    img_arr = np.array(img)  # 将图片转化为数组
    # 创建词云对象
    wc = WordCloud(
        width=1000, height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',
        mask=img_arr,
    )
    # 生成词云
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 保存词云图片到文件
    plt.savefig('./static/commentCloud.jpg', dpi=500)

# 获取舆情图表一数据（热词情感分析）
def getYuQingCharDataOne():
    # 获取热词列表
    hotWordList = getPublicData.getAllCiPingTotal()
    xData = ['正面', '中性', '负面']
    # 初始化各类情感的数量为0
    yData = [0,0,0]
    # 分析各热词的情感倾向
    for hotWord in hotWordList:
        emotionValue = SnowNLP(hotWord[0]).sentiments
        if emotionValue > 0.5:
            yData[0] +=1
        elif emotionValue == 0.5:
            yData[1] += 1
        elif emotionValue < 0.5:
            yData[2] += 1
    # 构造饼图数据
    bieData = [{
        'name': '正面',
        'value': yData[0]
    }, {
        'name': '中性',
        'value': yData[1]
    }, {
        'name': '负面',
        'value': yData[2]
    }]
    return xData,yData,bieData

# 获取舆情图表二数据（评论和文章情感分析）
def getYuQingCharDataTwo():
    # 初始化评论情感数据
    bieData1 = [{
        'name':'正面',
        'value':0
    },{
        'name':'中性',
        'value':0
    },{
        'name':'负面',
        'value':0
    }]
    # 初始化文章情感数据
    bieData2 = [{
        'name': '正面',
        'value': 0
    }, {
        'name': '中性',
        'value': 0
    }, {
        'name': '负面',
        'value': 0
    }]

    # 获取评论和文章数据
    commentList = getPublicData.getAllCommentsData()
    articleList = getPublicData.getAllData()

    # 分析评论情感倾向
    for comment in commentList:
        emotionValue = SnowNLP(comment[4]).sentiments
        if emotionValue > 0.5:
            bieData1[0]['value'] += 1
        elif emotionValue == 0.5:
            bieData1[1]['value'] += 1
        elif emotionValue < 0.5:
            bieData1[2]['value'] += 1
    # 分析文章情感倾向
    for article in articleList:
        emotionValue = SnowNLP(article[5]).sentiments
        if emotionValue > 0.5:
            bieData2[0]['value'] += 1
        elif emotionValue == 0.5:
            bieData2[1]['value'] += 1
        elif emotionValue < 0.5:
            bieData2[2]['value'] += 1

    return bieData1,bieData2

# 获取舆情图表三数据（热词频率）
def getYuQingCharDataThree():
    # 获取热词列表
    hotWordList = getPublicData.getAllCiPingTotal()
    # 返回热词名称和频率
    return [x[0] for x in hotWordList],[int(x[1]) for x in hotWordList]
