
#连接数据库
from flask_sqlalchemy import SQLAlchemy   #从 flask_sqlalchemy扩展包导入SQLAlchemy
import pymysql #导入第三方数据库
pymysql.install_as_MySQLdb() #把第三方数据库(pymysql)引擎替换为SQLAlchemy自带的引擎
# 创建Flask-SQLAlchemy的实例对象
db = SQLAlchemy()
class Config:
    # 开启调试模式
    DEBUG= False
#     指定数据库的连接地址
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/house"
#     压制警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False
