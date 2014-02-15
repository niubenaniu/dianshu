####说明####
**点书：**分享读书带来的乐趣与宁静

**点书**：微信公众号《点书》的后台自动服务程序
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
