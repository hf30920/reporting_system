from utils.getPublicData import *
from datetime import datetime
from snownlp import SnowNLP

# 获取表格页面热词数据
def getTableDataPageData():
    return getAllCiPingTotal()

# 根据热词获取相关评论数据
def getTableData(hotWord):
    # 获取所有评论数据
    commentList = getAllCommentsData()
    tableData =[]
    # 筛选包含指定热词的评论
    for comment in commentList:
        if comment[4].find(hotWord) != -1:
            tableData.append(comment)
    return tableData

# 获取表格数据图表数据
def getTableDataEchartsData(hotWord):
    # 获取表格数据
    tableList = getTableData(hotWord)
    # 获取唯一日期列表，并按时间倒序排列
    xData = [x[1] for x in tableList]
    xData = list(set(xData))
    xData = list(sorted(xData,key=lambda x:datetime.strptime(x,'%Y-%m-%d').timestamp(),reverse=True))
    # 初始化每天评论数为0
    yData = [0 for x in range(len(xData))]
    # 统计每天的评论数量
    for comment in tableList:
        for index,x in enumerate(xData):
            if comment[1] == x:
                yData[index] += 1
    return xData,yData

# 获取文章表格数据
def getTableDataArticle(flag):
    # 如果flag为真，则添加情感分析结果
    if flag:
        tableListOld = getAllData()
        tableList = []
        for item in tableListOld:
            item = list(item)
            # 使用SnowNLP进行情感分析
            emotionValue = SnowNLP(item[5]).sentiments
            if emotionValue > 0.5:
                emotionValue = '正面'
            elif emotionValue == 0.5:
                emotionValue = '中性'
            elif emotionValue < 0.5:
                emotionValue = '负面'
            item.append(emotionValue)
            tableList.append(item)
    else:
        # 直接获取所有文章数据
        tableList = getAllData()
    return tableList
