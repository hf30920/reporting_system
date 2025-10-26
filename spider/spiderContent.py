import time
import requests
import csv
import os
import re
from datetime import datetime

# 初始化函数，创建CSV文件并写入表头
def init():
    if not os.path.exists('articleData.csv'):
        with open('articleData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',# followBtnCode>uid + mblogid
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip' # v_plus
            ])

# 写入一行数据到CSV文件
def wirterRow(row):
        with open('articleData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

# 发送HTTP请求获取JSON数据
def get_json(url,params):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie':'XSRF-TOKEN=zSG69KfNFXoWtkWE9LF0obx_; _s_tentry=passport.weibo.com; appkey=; Apache=3344999134125.375.1720018458637; SINAGLOBAL=3344999134125.375.1720018458637; ULV=1720018458645:1:1:1:3344999134125.375.1720018458637:; PC_TOKEN=037e460a0a; SCF=AiC8Ti7pgnDBwnBrJaxekhNTBsB2C0n9SRrIzHI7pZxtc4ipPmSYdtGqL7BqP8OUmU8yulrjIV_lGTeW5-jCQDQ.; SUB=_2A25LwnmYDeRhGeFH6FIW9CfJzjqIHXVovvNQrDV8PUNbmtB-LXXCkW9Ne24CDCmXHwYoWm5uu6K6r1ycJuOOLuCc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4yCdrdy06aB2EyiCTqKKc5NHD95QN1Ke7S0B4SK-cWs4Dqcj3i--fi-2Xi-2Ni--NiKnRi-zpi--Xi-iFiK.4i--fi-z7iKyWP0.pe020; ALF=02_1726846664; WBPSESS=rISvH9geIeZF9eDvFdkIfvUYiKFMCGgP_TP4KhgncyWE6jAHqwYYCPXORPBKKQp3B-sdg3WiaRc0MoGrHZ9Mmru4qtZWr865DFRlBFIuXCurR1ZPn14LGSJsryxTRFS2EZV8AwDfw-SwcbfN2ISb5Q=='
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 解析JSON数据并写入CSV文件
def parse_json(response,type):
    for article in response:
        id = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于 ','')
        except:
            region = '无'
        content = article['text_raw']
        contentLen = article['textLength']
        created_at = datetime.strptime(article['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['user']['id']) +'/'+ str(article['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com' + article['user']['profile_url']
        if  article['user']['v_plus']:
            isVip = article['user']['v_plus']
        else:
            isVip = 0
        wirterRow([
                id,
                likeNum,
                commentsLen,
                reposts_count,
                region,
                content,
                contentLen,
                created_at,
                type,
                detailUrl,
                authorAvatar,
                authorName,
                authorDetail,
                isVip
            ])

# 启动爬虫函数
def start(typeNum=2,pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeNumCount = 0
    with open('./navData.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for nav in reader:
            if typeNumCount > typeNum:return
            for page in range(0,pageNum):
                time.sleep(2)
                print('正在爬取类型：' + nav[0] + '中的第' + str(page + 1) + '页数据')
                params = {
                    'group_id':nav[1],
                    'containerid':nav[2],
                    'max_id':page,
                    'count':10,
                    'extparam':'discover|new_feed'
                }
                response = get_json(articleUrl,params)
                parse_json(response['statuses'],nav[0])
            typeNumCount += 1

if __name__ == '__main__':
    start()