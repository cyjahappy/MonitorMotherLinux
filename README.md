# MonitorChildLinux
CRM服务器监控系统(母服务器端)

## 部署(Ubuntu 18.04)

#### 创建一个用于运行CRM服务器监控系统母服务器端Django Web App的用户

1. 创建用户

```
# 以monitor为例
$ adduser monitor
```

2. 赋予用户sudo权限:

    /etc/sudoers 追加一行(需要用强制保存)

```
monitor ALL=NOPASSWD: ALL
```

3. 切换到用户monitor

```
# 切换到用户
$ su monitor
```

#### 创建独立的Python虚拟环境

1. 安装virtualenv和virtualenvwrapper

```
$ sudo -H pip3 install virtualenv virtualenvwrapper
```

2. 创建目录用来存放虚拟环境

```
$ mkdir $HOME/.virtualenvs
```

3. 打开~/.bashrc文件，并添加内容：

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
```
 
4. 重新加载配置

```
$ source ~/.bashrc
```

5. 创建用于运行CRM服务器监控系统母服务器端Django Web App的Python虚拟环境

```
$ mkvirtualenv MonitorMotherLinux
```


```
# 相关命令:

# 切换到MonitorMotherLinux环境
$ workon MonitorMotherLinux

# 退出虚拟环境
$ deactivate
```

#### 部署Django Web App项目文件

1. 从[Realse - CRM监控系统(母服务器端)](https://github.com/cyjahappy/MonitorMotherLinux/releases)下载最新Django Web App项目文件

```
# 这里以v0.1-alpha版本为例
$ cd

$ wget https://github.com/cyjahappy/MonitorMotherLinux/archive/v0.1-alpha.zip
```

2. 将下载的压缩文件解压在该用户的主目录(这里是/home/monitor)

```
# 以v0.1-alpha为例
$ unzip v0.1-alpha.zip

# 将解压出来的文件夹重命名为MonitorMotherLinux(必须与之前创建的虚拟环境的名字一样)
$ mv MonitorMotherLinux-0.1-alpha MonitorMotherLinux

# 最终项目文件的位置应该是/home/monitor/MonitorMotherLinux
```

3. 安装依赖文件

```
# 进入项目文件的文件夹
$ cd /home/monitor/MonitorMotherLinux

# 进入刚才创建的名为MonitorMotherLinux的虚拟环境
$ workon MonitorMotherLinux

# 根据requrirements.txt安装依赖文件
$ pip3 install -r requirements.txt
```

4. 搜集静态文件

```
$ python manage.py collectstatic
```

5. 将/home/monitor/MonitorMotherLinux/MonitorMotherLinux/settings.py文件中ALLOWED_HOSTS= ['...']这栏中添加该服务器本机的公网IP地址(如果有域名的话也一并加上)

```
# 本例中服务器IP地址为157.245.176.143
ALLOWED_HOSTS = ['157.245.176.143']

# 本例中服务器IP地址为157.245.176.143, 域名为chenyuanjun.cn
ALLOWED_HOSTS = ['157.245.176.143',
                 'chenyuanjun.cn',
                 'www.chenyuanjun.cn']
```

5. 退出虚拟环境

```
$ deactivate
```

#### 安装uWSGI, 并配置开机启动

1. 系统级的安装uWSGI(不可在虚拟环境中安装)

```
$ sudo -H pip3 install uwsgi

# 检查版本
$ uwsgi --verison 
```

2. 创建uWSGI的配置文件
    在/home/monitor/MonitorMotherLinux文件夹中创建文件MonitorMotherLinux_uwsgi.ini, 并写入以下内容:

```
# MonitorMotherLinux_uwsgi.ini file
[uwsgi]

# Django-related settings
# Django项目文件夹绝对路径
chdir           = /home/monitor/MonitorMotherLinux
# Django的 wsgi 文件
module          = MonitorMotherLinux.wsgi
# Python虚拟环境的绝对路径
home            = /home/monitor/.virtualenvs/MonitorMotherLinux

# process-related settings
# master
master          = true
# 最大工作进程数
processes       = 10
# 存放uWSGI生成的Unix Socket的绝对路径
socket          = /home/monitor/MonitorMotherLinux/MonitorMotherLinux.sock
# 修改Unix Socket文件本身的权限
chmod-socket    = 777
# clear environment on exit
vacuum          = true
```

其中chmod-socket    = 777, 是为了方便Nginx调用uWSGI生成的Unix Socket. 如果不影响Nginx调用Unix Socket的话也可以设置为664或者666, 每个Linux系统对这块要求不一样(在母服务器中uWSGI进程的uid和gid可以不是root). 

3. 配置Emperor模式的uWSGI

```
# 为 vassals 创建一个文件夹
$ sudo mkdir /etc/uwsgi
$ sudo mkdir /etc/uwsgi/vassals

# 将刚才创建的uWSGI配置文件链接到/etc/uwsgi/vassals/
$ sudo ln -s /home/monitor/MonitorMotherLinux/MonitorMotherLinux_uwsgi.ini /etc/uwsgi/vassals/
```

4. 配置emperor.uwsgi.service(Systemd)

在/lib/systemd/system中创建emperor.uwsgi.service, 并写入以下内容:

```
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --ini /etc/uwsgi/emperor.ini
# Requires systemd version 211 or newer
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

5. 在/etc/uwsgi中创建文件emperor.ini, 并写入以下内容:

```
[uwsgi]
emperor = /etc/uwsgi/vassals
uid = monitor
gid = monitor
```

其中将uWSGI的进程用户和用户组设置为monitor. 

1. 运行以下指令

```
# 重载systemd daemon配置
$ sudo systemctl daemon-reload

# 配置uWSGI开机启动
$ sudo systemctl enable emperor.uwsgi.service

# 启动uWSGI
$ sudo systemctl start emperor.uwsgi.service
```

#### 配置Nginx

1. 在/etc/nginx/sites-enabled中创建文件MonitorMotherLinux_nginx.conf, 并写入以下内容:

```
# MonitorMotherLinux_nginx.conf
  
# the upstream component nginx needs to connect to
upstream django {
    # 指向刚才uWSGI创建的Unix Socket
    server unix:///home/monitor/MonitorMotherLinux/MonitorMotherLinux.sock; 
}

# configuration of the server
server {
    # Nginx对外监听的端口
    listen      80;
    # 该服务器的公网IP地址或者域名
    server_name 128.199.223.206;
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /static {
        alias /home/monitor/MonitorMotherLinux/static; # 指向Django项目存放静态文件的文件夹
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /home/monitor/MonitorMotherLinux/uwsgi_params; # 指向项目目录中的uwsgi_params 
    }
}
```

2. 从[nginx/uwsgi_params](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params)下载Nginx的uwsgi_params文件到Django Web App项目目录中(/home/monitor/MonitorChildLinux/uwsgi_params)

```
$ cd /home/monitor/MonitorMotherLinux
$ wget https://raw.githubusercontent.com/nginx/nginx/master/conf/uwsgi_params
```

4. 重启Nginx

```
$ sudo systemctl restart nginx
```

如果出错的话, 多半就是因为Nginx没有足够的权限去打开由uWSGI创建的Unix Socket. Nginx的进程的uid是www-data, uWSGI的进程的uid是monitor, 所以uWSGI创建的Unix Socket属于用户monitor. 在这里, 可以先尝试将www-data加入monitor的用户组, 同时也将monitor加入www-data的用户组. 

```
$ usermod -a -G monitor www-data
$ usermod -a -G www-data monitor

# 相互加入组后再重启一次Nginx
$ sudo systemctl restart nginx
```

如果还出错的话, 可以直接将Nginx进程的uid改成monitor. 打开/etc/nginx/nginx.conf, 在该文件第一行可以更改Nginx进程的uid, 将其改为monitor.

```
# /etc/nginx/nginx.conf的第一行
$ user monitor;
```

改完后重启Nginx, 如果没有报错的话说明成功. 可以在浏览器中打开:```{服务器公网IP地址}/admin```, 如果成功打开说明到目前为止的配置都没有问题.

#### 安装Redis

1. 使用 apt 从官方 Ubuntu 存储库来安装 Redis

```
$ sudo apt install redis-server
```

2. 配置Redis(Systemd)
   
打开Redis的配置文件

```
$ sudo vim /etc/redis/redis.conf
```

在文件中，找到supervised指令。 该指令允许我们声明一个init系统来管理Redis作为服务，从而为我们提供对其操作的更多控制。 受supervised指令默认设置为no 。 由于我们正在运行使用systemd init系统的Ubuntu，请将其更改为systemd ：

```
# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd
```

3. 重新加载Redis服务文件以反映您对配置文件所做的更改：

```
$ sudo service redis restart
```

4. 查看Redis的运行状态

```
$ sudo systemctl status redis
```

如果显示如下结果表示成功:

```
● redis-server.service - Advanced key-value store
   Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-06-04 02:02:24 UTC; 4s ago
     Docs: http://redis.io/documentation,
           man:redis-server(1)
  Process: 18354 ExecStop=/bin/kill -s TERM $MAINPID (code=exited, status=0/SUCCESS)
  Process: 18358 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
 Main PID: 18370 (redis-server)
    Tasks: 4 (limit: 1152)
   CGroup: /system.slice/redis-server.service
           └─18370 /usr/bin/redis-server 127.0.0.1:6379

Jun 04 02:02:24 ubuntu-Singapore2 systemd[1]: Starting Advanced key-value store...
Jun 04 02:02:24 ubuntu-Singapore2 systemd[1]: redis-server.service: Can't open PID file /var/run/redis/redis-server.pid (yet?) after start: No 
Jun 04 02:02:24 ubuntu-Singapore2 systemd[1]: Started Advanced key-value store.
```

#### 配置Celery(Systemd)

1. 配置Celery的Systemd文件

在/lib/systemd/system中创建文件celery.service

```
$ sudo vim /lib/systemd/system/celery.service
```

 写入以下内容:

```
[Unit]
Description=Celery Service
After=network.target

[Service]
User=monitor
Group=monitor
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/home/monitor/MonitorMotherLinux
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} worker --pidfile=${CELERYD_PID_FILE}\
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS} -P eventlet'

[Install]
WantedBy=multi-user.target
```

2. 编辑Celery配置文件

在/etc/conf.d中创建文件celery

```
$ sudo vim /etc/conf.d/celery
```

写入以下内容:

```
# 指向Python虚拟环境中celery的二进制文件的绝对路径
CELERY_BIN="/home/monitor/.virtualenvs/MonitorMotherLinux/bin/celery"

# App示例的名字
CELERY_APP="MonitorMotherLinux"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
# 指向Celery的PID文件和LOG文件的绝对路径
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"

# 指向Celery Beat的PID文件和LOG文件的绝对路径
CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
```

3. 配置Celery Beat 的Systemd文件

在/lib/systemd/system中创建文件celerybeat.service

```
$ sudo vim /lib/systemd/system/celerybeat.service
```

 写入以下内容:

```
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=monitor
Group=monitor
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/home/monitor/MonitorMotherLinux
ExecStart=/bin/sh -c '${CELERY_BIN} beat  \
  -A ${CELERY_APP} --pidfile=${CELERYBEAT_PID_FILE} \
  --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} -S django'

[Install]
WantedBy=multi-user.target
```

4. 重载Daemon配置, 并配置开机启动

```
# 重载systemd daemon配置
$ sudo systemctl daemon-reload

# 配置Celery开机启动
$ sudo systemctl enable celery.service

# 配置Celery Beat开机启动
$ sudo systemctl enable celerybeat.service

# 启动Celery
$ sudo systemctl start celery.service

# 启动Celery Beat
$ sudo systemctl start celerybeat.service
```