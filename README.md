***
####这是什么####
**点书：** 微信公众号《点书》的后台自动服务程序

**主页：** <http://115.28.3.240/weixin/home/>

**未完成功能**

1. 微信后台程序的图书详情页面前端

2. 历史文章列表查询功能

3. 腾讯微博爬虫

***
####技术清单####
+ **前端：** HTML5、Bootstrap 3.0.3、CSS、jQuery 1.10.2、JavaScript
+ **图表：** Highcharts
+ **后端：** Python 2.7.3、Django 1.6
+ **数据库：** MongoDB 2.0.4
+ **Web服务器：** Nginx 1.1.19
+ **操作系统：** Ubuntu 12.04.1 LTS

***
####环境清单：####
1. **Pycurl**
    <pre>apt-get install python-pycurl<code>
2. **simplejson**
    <pre>apt-get install python-simplejson<code>
3. **Pillow**

    **Pillow是Python的图片处理模块。**
    <pre>apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev
    sudo ln -s /usr/lib/`uname -i`-linux-gnu /libfreetype.so /usr/lib/
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
    apt-get install python-dev
    pip install Pillow<code>
4. **Git**
    <pre>apt-get install git<code>
5. **MySQL**
    <pre>apt-get install mysql-server
    usr:root<code>
6. **Django**
    <pre>apt-get install python-pip
    pip install Django==1.6<code>
7. **Django_auth:auth_admin_dianshu**
    <pre>usr：admin
    email：niubenaniu@gmail.com<code>
8. **Django-MySQL**
    <pre>apt-get install  python-mysqldb<code>
9. **Django-Nginx**
    <pre>apt-get install nginx python-flup<code>
10. **Nginx**
    <pre>apt-get install gcc
    apt-get install g++
    curl -O <ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.33.tar.gz>
    curl -O zlib.net/zlib-1.2.8.tar.gz
    curl -O nginx.org/download/nginx-1.4.4.tar.gz
安装：
    tar -xzvf xxxx
    cd xxxx
    ./configure
    make
    make install
启动：
    /usr/local/nginx/sbin/nginx<code>
