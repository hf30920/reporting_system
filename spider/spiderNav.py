import requests
import csv
import os
import numpy as np

# 初始化函数，创建CSV文件并写入表头
def init():
    if not os.path.exists('navData.csv'):
        with open('navData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'typeName',
                'gid',
                'containerid'
            ])

# 写入一行数据到CSV文件
def wirterRow(row):
        with open('navData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

# 发送HTTP请求获取JSON数据
def get_html(url):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Cookie':'XSRF-TOKEN=zSG69KfNFXoWtkWE9LF0obx_; PC_TOKEN=a776459803; _s_tentry=passport.weibo.com; appkey=; Apache=3344999134125.375.1720018458637; SINAGLOBAL=3344999134125.375.1720018458637; ULV=1720018458645:1:1:1:3344999134125.375.1720018458637:; geetest_token=27f4d5060d7fd17140c1ab0d71565394; ALF=1722610500; SUB=_2A25LgRYUDeRhGeFH6FIW9CfJzjqIHXVo_xfcrDV8PUJbkNAbLW_gkW1Ne24CDHSisvyp623B6BuzKvTehDpA8qLW; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4yCdrdy06aB2EyiCTqKKc5JpX5KzhUgL.FoM4e05NSh.fSKq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM7eh2RSh.4eK2f; WBPSESS=rISvH9geIeZF9eDvFdkIfvUYiKFMCGgP_TP4KhgncyWE6jAHqwYYCPXORPBKKQp3B-sdg3WiaRc0MoGrHZ9MmtDhfZWW8KZnUyGJVhNa1762HewTzxX3WzlShxIGGIoZ2aCWhM6L_T7CsE1jWHHU9A=='
    }
    params = {
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 解析JSON数据并写入CSV文件
def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        wirterRow([
            navName,
            gid,
            containerid,
        ])

if __name__ == '__main__':
    url = 'https://weibo.com/ajax/feed/allGroups'
    init()
    response = get_html(url)
    parse_json(response)