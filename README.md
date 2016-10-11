# Here用户手册

标签（空格分隔）： Here Flask Python Android

---
## 1.安装与部署
### 1.1 构建Flask虚拟环境
一般Linux发行版都会预安装Python，在Terminal输入Python获取对应版本
```
python -V
```
若如未安装Python，或如部分CentOS等发行版预装版本不为Python2.7.6，在[Python官网](https://www.python.org/download/releases/2.7.6/)下载XZ compressed source tar ball (2.7.6) (sig)编译安装
```
tar xvf Python-2.7.6.tar
cd Python-2.7.6
./configure
make
make install
```
下载后的hereServer文件结构如下
```
└── app # 应用目录
    ├── __init__.py 
    ├── models.py # ORM
    ├── static # CSS等静态
    ├── templates # 模板
    ├── views.py # 视图
    └── *.py # 用于邮件等
├── tmp # 日志等文件记录目录
├── uploads # 上传照片目录
├── config.py # 应用配置文件
├── db_*.py # 数据库相关操作文件
├── runserver.py # 服务启动文件
└── *.py # 其他文件用于测试等
```
安装virtualenv
```
sudo apt-get install python-virtualenv
```
在下载后的hereServer目录下，生成虚拟环境
```
virtualenv flask/
```
仍然在hereServer目录下，安装Flask及其插件到虚拟环境（网络不好安装失败可以重复运行）
```
flask/bin/pip install flask==0.9
flask/bin/pip install flask-login
flask/bin/pip install flask-mail
flask/bin/pip install sqlalchemy==0.7.9
flask/bin/pip install flask-sqlalchemy==0.16
flask/bin/pip install sqlalchemy-migrate
flask/bin/pip install flask-wtf
flask/bin/pip install pytz==2013b
flask/bin/pip install flup
flask/bin/pip install flask-httpauth
flask/bin/pip install passlib
```
仍然在hereServer目录下，生成数据库
```
./db_create.py
```
在`config.py`中配置服务器其他信息
```
# mail config
TURN_ON_MAIL = False # 开启mail
MAIL_SERVER = 'smtp.googlemail.com' # smtp服务器，这里默认是一个gmail配置
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'google username' # smtp服务邮箱的账号
MAIL_PASSWORD = 'google password' # smtp服务邮箱的密码
```
在`db_create.py`中配置初次使用管理员的账户密码等信息(在下一个update后会修改这种方式)
```
user = User(nickname = 'admin', 
        email = 'admin@example.com',
        role = ROLE_ADMIN)
user.hash_password('123456')
```
### 1.2 Linux生产环境下Server端
安装Nginx、uUWSGI和uWSGI Python扩展，这里仅仅是一个参照部署方式，更多部署请参考[Flask文档](http://dormousehole.readthedocs.org/en/latest/deploying/index.html)
```
sudo apt-get install nginx
sudo apt-get install uwsgi uwsgi-plugin-python
```
修改`/etc/nginx/nginx.conf`，（**注意**：下面的文件修改都有可能需要使用root权限）
```
...

http {
    ...
    ##
    # Virtual Host Configs
    ##

    #include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*.conf;
}
```
创建`/etc/nginx/sites-enabled/www.xxx.com.conf`，其中www.xxx.com为主机名，可以在`/etc/hosts`中加入主机名
```
server {
    listen 80;
    server_name www.xxx.com xxx.com;
    access_log /var/log/nginx/www.xxx.com.access.log;
    error_log /var/log/nginx/www.xxx.com.error.log;
    location /
    {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi_www.xxx.com.sock;
    }
}
```
创建`/etc/uwsgi/apps-enabled/www.xxx.com.ini`
```
[uwsgi]
plugins = python
vhost = true
chmod-socket = 666
socket = /tmp/uwsgi_www.xxx.com.sock
venv = /var/www/hereServer/flask
chdir = /var/www/hereServer
module = runserver
callable = app
```
将hereServer文件夹拷贝到`/var/www/`下，并修改权限和用户，之后重启服务
```
sudo chmod -R 775 /var/www/hereServer/
sudo chown -R www-data:www-data /var/www/hereServer/
sudo service nginx restart
sudu service uwsgi restart
```

### 1.3 Windows测试下Server端
强烈不建议在Windows下部署生产环境，仅仅用于测试
先安装Python2.7.6，在[Python官网](https://www.python.org/download/releases/2.7.6/)下载对应Windows环境的Installer.msi文件，运行文件默认安装，在cmd命令中输入检查是否正确安装
```
python -V
```
在hereServer中提供了`testWinSetup.py`脚本配置（**注意**：这个脚本仅仅用于Windows测试环境配置），需要在管理员模式运行，如下命令可能会需要配置Administrator的密码
```
net user administrator /active:yes  # 打开管理员账户
runas /noprofile /user:Administrator cmd  # 进入管理员模式
```
在cmd中切换到hereServer目录，执行`testWinSetup.py`配置虚拟环境并安装Flask及其扩展
```
python testWinSetup.py
```
在cmd中切换到hereServer目录,使用虚拟环境的Python解释器创建数据库和启动服务
```
flask\Scripts\python testWinSetup.py
flask\Scripts\python run.py
```
在`config.py`中配置服务器其他信息，配置后重新启动服务（对于测试服务器，可以配置测试可视范围和测试端口）
```
# mail config
TURN_ON_MAIL = False # 开启mail
MAIL_SERVER = 'smtp.googlemail.com' # smtp服务器，这里默认是一个gmail配置
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'google username' # smtp服务邮箱的账号
MAIL_PASSWORD = 'google password' # smtp服务邮箱的密码

# server config 
SERVER_PORT = 5000 # 服务启动端口
SERVER_VISION = '0.0.0.0'
```

---
## 2.Web端使用
1.对于初次安装后会生成admin账户，使用admin账户登录
2.admin账户可以注册修改用户和课程
3.注册课程后可以在课程页面的edit中编辑参加课程的学生
4.教师具有查看课程和学生的功能，但是不能注册和修改课程以及学生
5.学生账户通过web端只能查看自己的页面信息

---
## 3.Android端使用
1.Android只针对学生使用，通过nickname和password登录
2.首次使用需要在登录页面的setting中配置服务器地址和端口（这会在下一个update修改，直接配置服务器名称即可）
3.进入页面后会有可以列表，点击列表即可对当即课程签到，在新的课程信息页面会有照相并上传的功能
4.每门课程的点名时间是课程开始前的半个小时，如果不在点名时间区间则会提示
