1. 安装环境
pip install aliyun-python-sdk-sts
pip install aliyun-python-sdk-mts
pip install aliyun-python-sdk-core
pip install oss2
pip install tornado
pip install supervisor
wget https://pypi.python.org/packages/source/M/MySQL-python/MySQL-python-1.2.5.zip#md5=654f75b302db6ed8dc5a898c625e030c
yum install unzip
unzip MySQL-python-1.2.5.zip
yum install python-devel
yum install mysql-devel
yum -y install mysql-devel
python setup.py build
python setup.py install
yum install nginx

pip install sqlalchemy
pip install greenlet
pip install pytz


wget http://repo.mysql.com/mysql57-community-release-el7-8.noarch.rpm
rpm -ivh mysql57-community-release-el7-8.noarch.rpm
yum install mysql-server
systemctl  start mysqld
grep "password" /var/log/mysqld.log
SET PASSWORD = PASSWORD('123456');

upstream servers.mydomain.com {
    server localhost:8085;
    server localhost:8086;
}
server{
    listen 8081;
    server_name 119.23.77.222;
    location / {
        proxy_pass http://servers.mydomain.com;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
