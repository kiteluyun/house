
from flask import Flask, render_template,Blueprint, request,jsonify
from sqlalchemy import func
from models import House
# 创建蓝图，蓝图的名称为包的名称 ，即index_page
index_page = Blueprint('index_page', __name__)
@index_page.route('/')
def index():
    house_tatal_num = House.query.count()   #获取房源总数
     
    # 获取最新房源
    house_new_list=House.query.order_by(
        House.publish_time.desc()).limit(6).all()
     
    # 获取最热房源
    house_hot_list=House.query.order_by(
       House.page_views.desc()).limit(4).all()
    return render_template('index.html',num=house_tatal_num,house_new_list=house_new_list,house_hot_list=house_hot_list)
 
# 查找相应关键字
@index_page.route('/search/keyword/',methods=['POST'])
def seach_kw():
    kw=request.form['kw']  #获取搜索关键字
    info=request.form['info']  #获取用户选择的搜索选项
    if info=='地区搜索':
        # 获取查询的结果
        house_data=House.query.with_entities(
            House.address,func.count()).filter(House.address.contains(kw))
        # 对查询的结果进行分组，排序，并获取最多9条房源数据

        result=house_data.group_by('address').order_by(
            func.count().desc()).limit(9).all()
        if len(result):
            data=[]
            for i in result:
                # 将查询到的房源数据添加到data列表中
                data.append({'t_name':i[0],'num':i[1]})
            return jsonify({'code':1,'info':data})
        else:  #没有查询结果
            return jsonify({'code':0,'info':[]})
    if info == '户型搜索':
            house_data=House.query.with_entities(
                House.rooms,func.count()).filter(House.rooms.contains(kw))
            result=house_data.group_by('rooms').order_by(
                func.count().desc()).limit(9).all()
            if len(result):
                data=[]
                for i in result:
                    data.append({'t_name':i[0],'num':i[1]})
                return jsonify({'code':1,'info':data})
            else:
                return jsonify({'code':0,'info':[]})