import requests
import csv
import os
from datetime import datetime

# 初始化函数，创建CSV文件并写入表头
def init():
    if not os.path.exists('commentsData.csv'):
        with open('commentsData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'articleId',
                'created_at',
                'like_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

# 写入一行数据到CSV文件
def wirterRow(row):
        with open('commentsData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

# 发送HTTP请求获取JSON数据
def get_html(url,id):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'Cookie':'XSRF-TOKEN=zSG69KfNFXoWtkWE9LF0obx_; _s_tentry=passport.weibo.com; appkey=; Apache=3344999134125.375.1720018458637; SINAGLOBAL=3344999134125.375.1720018458637; ULV=1720018458645:1:1:1:3344999134125.375.1720018458637:; PC_TOKEN=037e460a0a; SCF=AiC8Ti7pgnDBwnBrJaxekhNTBsB2C0n9SRrIzHI7pZxtc4ipPmSYdtGqL7BqP8OUmU8yulrjIV_lGTeW5-jCQDQ.; SUB=_2A25LwnmYDeRhGeFH6FIW9CfJzjqIHXVovvNQrDV8PUNbmtB-LXXCkW9Ne24CDCmXHwYoWm5uu6K6r1ycJuOOLuCc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4yCdrdy06aB2EyiCTqKKc5NHD95QN1Ke7S0B4SK-cWs4Dqcj3i--fi-2Xi-2Ni--NiKnRi-zpi--Xi-iFiK.4i--fi-z7iKyWP0.pe020; ALF=02_1726846664; WBPSESS=rISvH9geIeZF9eDvFdkIfvUYiKFMCGgP_TP4KhgncyWE6jAHqwYYCPXORPBKKQp3B-sdg3WiaRc0MoGrHZ9Mmru4qtZWr865DFRlBFIuXCurR1ZPn14LGSJsryxTRFS2EZV8AwDfw-SwcbfN2ISb5Q=='
    }
    params = {
        'is_show_bulletin':2,
        'id':id
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 解析JSON数据并写入CSV文件
def parse_json(response,articleId):
    commentList = response['data']
    for comment in commentList:
        created_at = datetime.strptime(comment['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        like_counts = comment['like_counts']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location'].split(' ')[0]
        authorAvatar = comment['user']['avatar_large']
        try:
            region = comment['source'].replace('来自','')
        except:
            region = '无'
        content = comment['text_raw']
        wirterRow([
            articleId,
            created_at,
            like_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar,
        ])

# 启动爬虫函数
def start():
    init()
    url = 'https://weibo.com/ajax/statuses/buildComments'
    with open('./articleData.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for article in reader:
            articleId = article[0]
            response = get_html(url,articleId)
            parse_json(response,articleId)


if __name__ == '__main__':
    start()