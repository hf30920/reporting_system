from flask import Flask,session,render_template,redirect,Blueprint,request
from utils import getHomeData,getTableData,getEchartsData
from snownlp import SnowNLP
# 创建页面蓝图
pb = Blueprint('page',__name__,url_prefix='/page',template_folder='templates')

# 主页路由
@pb.route('/home')
def home():
    # 获取当前登录用户名
    username = session.get('username')
    # 获取点赞数最高的前几条评论
    topFiveComments = getHomeData.getHomeTopLikeCommentsData()
    # 获取文章总数、最多点赞作者名、最多文章的城市
    articleLen,maxLikeAuthorName,maxCity = getHomeData.getTagData()
    # 获取文章创建数量图表数据
    xData,yData = getHomeData.getCreatedNumEchartsData()
    # 获取用户创建类型图表数据
    userCreatedDicData = getHomeData.getTypeCharData()
    # 获取评论用户创建数量图表数据
    commentUserCreatedDicData = getHomeData.getCommentsUserCratedNumEchartsData()
    # 返回主页模板及数据
    return render_template('index.html'
                           ,username=username,
                           topFiveComments=topFiveComments,
                           articleLen=articleLen,
                           maxLikeAuthorName=maxLikeAuthorName,
                           maxCity=maxCity,
                           xData=xData,
                           yData=yData,
                           commentUserCreatedDicData=commentUserCreatedDicData,
                           userCreatedDicData=userCreatedDicData
                           )

# 表格数据页面路由
@pb.route('/tableData')
def tabelData():
    # 获取当前登录用户名
    username = session.get('username')
    # 获取热门词汇列表
    hotWordList = getTableData.getTableDataPageData()
    # 默认选中第一个热词
    defaultHotWord = hotWordList[0][0]
    # 如果URL中有指定热词，则使用指定的热词
    if request.args.get('hotWord'):defaultHotWord = request.args.get('hotWord')
    # 查找默认热词的数量
    defaultHotWordNum = 0
    for hotWord in hotWordList:
        if defaultHotWord == hotWord[0]:defaultHotWordNum=hotWord[1]
    # 使用SnowNLP分析热词情感
    emotionValue = SnowNLP(defaultHotWord).sentiments
    if emotionValue > 0.5:
        emotionValue = '正面'
    elif emotionValue == 0.5:
        emotionValue = '中性'
    elif emotionValue < 0.5:
        emotionValue = '负面'
    # 获取表格数据
    tableList = getTableData.getTableData(defaultHotWord)
    # 获取表格数据图表数据
    xData,yData = getTableData.getTableDataEchartsData(defaultHotWord)
    # 返回表格数据页面模板及数据
    return render_template('tableData.html',
                           username=username,
                           hotWordList=hotWordList,
                           defaultHotWord=defaultHotWord,
                           defaultHotWordNum=defaultHotWordNum,
                           emotionValue=emotionValue,
                           tableList=tableList,
                           xData=xData,
                           yData=yData
                           )

# 文章表格数据页面路由
@pb.route('/tableDataArticle')
def tableDataArticle():
    # 获取当前登录用户名
    username = session.get('username')
    # 默认标志位为False
    defaultFlag = False
    # 如果URL中有指定标志位，则使用指定的标志位
    if request.args.get('flag'):defaultFlag = request.args.get('flag')
    # 获取文章表格数据
    tableData = getTableData.getTableDataArticle(defaultFlag)
    # 返回文章表格数据页面模板及数据
    return render_template('tableDataArticle.html',
                           username=username,
                           defaultFlag=defaultFlag,
                           tableData=tableData
                           )

# 文章图表页面路由
@pb.route('/articleChar')
def articleChar():
    # 获取当前登录用户名
    username = session.get('username')
    # 获取文章类型列表
    typeList = getEchartsData.getTypeList()
    # 默认选中第一个类型
    defaultType = typeList[0]
    # 如果URL中有指定类型，则使用指定的类型
    if request.args.get('type'): defaultType = request.args.get('type')
    # 获取文章图表数据
    xData,yData = getEchartsData.getArticleCharOneData(defaultType)
    x1Data,y1Data = getEchartsData.getArticleCharTwoData(defaultType)
    x2Data,y2Data = getEchartsData.getArticleCharThreeData(defaultType)
    # 返回文章图表页面模板及数据
    return render_template('articleChar.html',
                           username=username,
                           typeList=typeList,
                           defaultType=defaultType,
                           xData=xData,
                           yData=yData,
                           x1Data=x1Data,
                           y1Data=y1Data,
                           x2Data=x2Data,
                           y2Data=y2Data
                           )

# IP图表页面路由
@pb.route('/ipChar')
def ipChar():
    # 获取当前登录用户名
    username = session.get('username')
    # 获取地理位置图表数据
    geoDataOne = getEchartsData.getGeoCharDataOne()
    geoDataTwo = getEchartsData.getGeoCharDataTwo()
    # 返回IP图表页面模板及数据
    return render_template('ipChar.html',
                           username=username,
                           geoDataOne=geoDataOne,
                           geoDataTwo=geoDataTwo
                           )


# 评论图表页面路由
@pb.route('/commentChar')
def commentChar():
    # 获取当前登录用户名
    username = session.get('username')
    # 获取评论图表数据
    xData,yData = getEchartsData.getCommetCharDataOne()
    genderDicData = getEchartsData.getCommetCharDataTwo()
    # 返回评论图表页面模板及数据
    return render_template('commentChar.html',
                           username=username,
                           xData=xData,
                           yData=yData,
                           genderDicData=genderDicData
                           )

# 舆情图表页面路由
@pb.route('/yuqingChar')
def yuqingChar():
    # 获取当前登录用户名
    username = session.get('username')
    # 获取舆情图表数据
    xData,yData,bieData = getEchartsData.getYuQingCharDataOne()
    bieData1, bieData2 = getEchartsData.getYuQingCharDataTwo()
    x1Data,y1Data = getEchartsData.getYuQingCharDataThree()
    # 返回舆情图表页面模板及数据
    return render_template('yuqingChar.html',
                           username=username,
                           xData=xData,
                           yData=yData,
                           bieData=bieData,
                           bieData1=bieData1,
                           bieData2=bieData2,
                           x1Data=x1Data[:10],
                           y1Data=y1Data[:10]
                           )

# 内容云图页面路由
@pb.route('/contentCloud')
def contentCloud():
    # 获取当前登录用户名
    username = session.get('username')
    # 返回内容云图页面模板
    return render_template('contentCloud.html',
                           username=username
                           )