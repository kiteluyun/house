
from flask import Flask,render_template
# 从settings.py文件中导入配置Config类
from settings import Config,db
from models import House
from index_page import index_page  #导入蓝图index_page模块
from list_page import list_page
from detail_page import detail_page
from user_page import user_page
from sklearn.linear_model import LinearRegression


app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app) #用于初始化Flask应用程序与数据库的关联，以便在应用程序中访问数据库进行数据操作
app.register_blueprint(index_page,url_prefix='/')  #注册蓝图index_page
app.register_blueprint(list_page,url_prefix='/')
app.register_blueprint(detail_page,url_prefix='/')
app.register_blueprint(user_page,url_prefix='/')
# 测试的视图函数
@app.route('/')
def test():
    first_user = House.query.first()
    print(first_user)
    return 'OK'
# @app.route('/test')
# def test1():
#     return render_template('test.html')
if __name__ == '__main__':
    app.run(debug=True)



