import bdb
from datetime import datetime, timedelta
from settings import db
from flask import Blueprint, render_template, jsonify,request
from sqlalchemy import func
from models import  House,User
from regression_data import linear_model_main
detail_page=Blueprint('detail_page',__name__)
# @detail_page.route('/house/<int:hid>')
# def detail(hid):
#     # 查询数据库
#     house=House.query.get(hid)
#     facilities_str=house.facilities
#     facilities_list=facilities_str.split('-')
#     return render_template('detail_page.html',house=house,facilities=facilities_list)
def deal_traffic_txt(word):
    if len(word)==0 or word is None:
        return '暂无信息!'
    else:
        return word

@detail_page.route('/get/piedata/<block>')
def return_pie_data(block):  # 查询数据库
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(
    House.rooms).order_by(func.count().desc()).all()
    data = []
    for one_house in result:
        data.append({'name': one_house[0], 'value': one_house[1]})
    return jsonify({'data': data})

@detail_page.route('/get/columndata/<block>')
def return_bar_data(block):
    result=House.query.with_entities(House.address,func.count()).filter(House.block==block).group_by(House.address).order_by(func.count().desc()).all()
    name_list=[]
    num_list=[]
    for addr,num in result:
        residence_name=addr.rsplit('-',1)[1]
        name_list.append(residence_name)
        num_list.append(num)
    if len(name_list)>20:
        data={'name_list_x':name_list[:20],'num_list_y':num_list[:20]}
    else:
        data={'name_list_x':name_list,'num_list_y':num_list}
    return jsonify({'data':data})




@detail_page.route('/get/brokenlinetdata/<block>')
def return_brokenline_data(block):
    time_stamp=House.querxy.filter(House.block==block).with_entities(House.publish_time).all()
    time_stamp.sort(reverse=True)
    data_li=[]
    for i in range(1,14):
        latest_release=datetime.fromtimestamp(int(time_stamp[0][0]))
        day=latest_release+timedelta(days=-i)
        date_li.append(day.strftime('%m-%d'))
    date_li.reverse()
    result= House.query.with_entities(
        func.avg(House.price/House.area)).filter(House.block==block,House.rooms=='1室1厅').group_by(House.publish_time).order_by(House.publish_time).all()
    data=[]
    for i in result[-14:]:
        data.append(round(i[0],2))
    result1= House.query.with_entities(
        func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '2室1厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data1 = []
    for i in result[-14:]:
        data.append(round(i[0], 2))
    result2 = House.query.with_entities(
        func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '2室2厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data2 = []
    for i in result[-14:]:
        data.append(round(i[0], 2))
    result3 = House.query.with_entities(
        func.avg(House.price / House.area)).filter(House.block == block, House.rooms == '3室2厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data3 = []
    for i in result[-14:]:
        data.append(round(i[0], 2))
    return jsonify({'data':{'1室1厅':data,'2室1厅':data1,'2室2厅':data2,'3室2厅':data3,'date_li':date_li}})


@detail_page.route('/get/scatterdata/<block>')
def return_scatter_data(block):
    result=House.query.with_entities(func.avg(House.price/House.area)).filter(House.block==block).group_by(House.publish_time).order_by(House.publish_time).all()
    time_stamp=House.query.filter(House.block==block).with_entities(House.publish_time).all()
    time_stamp.sort(reverse=True)
    date_li=[]
    for i in range(1,30):
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        day=latest_release+timedelta(days=-i)
        date_li.append(day.strftime('%m-%d'))
    date_li.reverse()
    data=[]
    x=[]
    y=[]
    for index,i in enumerate(result):
        x.append([index])
        y.append(round(i[0],2))
        data.append([index,round(i[0],2)])
    predict_value=len(data)
    predict_outcome=linear_model_main(x,y,predict_value)
    p_outcome=round(predict_outcome[0],2)
    data.append([predict_value,p_outcome])
    return jsonify({'data':{'data-predict':data,'date_li':date_li}})





def deal_traffic_txt(word):
    if len(word)==0 or word is None:
        return '暂无信息!'
    else:
        return word
detail_page.add_app_template_filter(deal_traffic_txt,'dealNone')





@detail_page.route('/house/<int:hid>')
def detail(hid):
    house = House.query.get(hid)
    facilities_str = house.facilities
    facilities_list=facilities_str.split('-')
    name = request.cookies.get('name')
    if name:
        user = User.query.filter(User.name==name).first()
        seen_id_str = user.seen_id
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')
            set_id = set([int(i) for i in seen_id_list])
            if hid not in set_id:
                new_seen_id_str = seen_id_str+','+str(hid)
                user.seen_id = new_seen_id_str
                db.session.commit()
        else:
            user.seen_id = str(hid)
            db.session.commit()
    return render_template('detail_page.html',house=house,facilities=facilities_list)


