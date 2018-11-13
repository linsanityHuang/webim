#Web-IM

##介绍
这是一个web端即时通讯，目前尚处于开发过程中，主体功能已经完成，但是一些细节功能尚需优化和补充。
目前该项目已经部署在阿里云，部署方案采用Nginx+supervisor+daphne+gunicorn, 如需体验请访问https://iwantme.cn


##功能介绍

1. 私聊
2. 群聊
3. 发送图片和文件
4. 搜索并添加好友
5. 用户注册及登录
6. 用户资料修改
7. 限制文件上传的大小及类型

##技术栈

### 后端
1. Django
2. Channels
3. Nginx
4. Redis
5. MySQL
6. Docker

### 前端
#######由于前端框架需要获得授权，所以此开源项目并不包括前端代码
1. <a href="https://layim.layui.com/" target="_blank">LayIM</a>(已获得授权)
2. <a href="https://www.layui.com/" target="_blank">LayUI</a>(开源)


##待实现功能

1. 客服
2. 聊天机器人

##部署准备

###安装依赖
1. python3.6
2. pip install -r requirements.txt

###数据库(docker container)
1. MySQL
***
运行MySQL容器
`docker run --name docker-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql`
***
进入MySQL容器
`docker exec -it docker-mysql mysql -uroot -p`

`create database webim default character set utf8 collate utf8_general_ci;`

`python manage.py makemigrations chat`
`python manage.py migrate chat`

2. Redis
***
`docker run --name docker-redis -p 6379:6379 -d redis`

###配置文件
1. setting.py (Debug = True, Domain)