# 项目部署

## 1.数据库建立
    打开MySQL数据库（类似Navicat Premium），登录后,创立一个名为’wb’的数据库，运行“数据库”文件夹中提供的sql文件建立数据库并且初始化数据的，成功运行后应该有三张含有数据的表

## 2. 数据库配置项修改

    配置’ /utils/query’和’ /spider/main’目录下的python文件头部的数据库连接部分，修改密码和数据库名称（默认为wb）

## 3.项目后端数据爬取+处理
    在’ /spider/spiderComments.py’，’spider/spiderContent.py’，’spider/spiderNav.py’中，更改请求头。header中的'User-Agent'和'Cookie'要更新，具体看视频中的介绍
    
    运行’spider/main.py’

## 4.python环境准备
    选择一个python的虚拟环境作为解释器，确保里面含有必须的模块，具体可见environment.yml文件，用pip指令安装即可

## 5.项目启动
    调试配置选择Python调试程序：Flask，启动项目，浏览器访问http://127.0.0.1:5000，注册账号后即可登录