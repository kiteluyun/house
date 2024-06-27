
from flask import Blueprint,request,render_template
from models import House
import math
# 创建一个蓝图对象
list_page= Blueprint('list_page', __name__)
@list_page.route('/query')
def search_txt_info():
    if request.args.get('addr'):
        addr=request.args.get('addr')
        result=House.query.filter(House.address==addr).order_by(House.publish_time.desc()).all()
        return render_template('search_list.html',house_list=result)
    if request.args.get('rooms'):
        rooms_info=request.args.get('rooms')
        result=House.query.filter(House.rooms==rooms_info).order_by(House.publish_time.desc()).all()
        return render_template('search_list.html',house_list=result)
#     2021011008  胡珂静
@list_page.route('/list/pattern/<int:page>')
def return_new_list(page):
    house_num=House.query.count()
    total_num=math.ceil(house_num/10)
    result=House.query.order_by(House.publish_time.desc()).paginate(page=page,per_page=10)
    return render_template('list.html',house_list=result.items,page_num=result.page,total_num=total_num)
  
@list_page.route('/list/hot_house/<int:page>')
def return_hot_list(page):
    house_num=House.query.count()
    total_num=math.ceil(house_num/10)
    result=House.query.order_by(House.page_views.desc()).paginate(page=page,per_page=10)
    return render_template('list.html',house_list=result.items,page_num=result.page,total_num=total_num)
  
def deal_title_over(word):
    if len(word)>15:
        return word[:15]+'...'
    else:
        return word
def deal_direction(word):
    if len(word)==0 or word is None:
        return '暂无信息'
    else:
        return word
list_page.add_app_template_filter(deal_title_over,'dealover')
list_page.add_app_template_filter(deal_direction,'dealdirection')

