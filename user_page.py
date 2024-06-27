from flask import Blueprint, request, Response, jsonify, render_template,redirect
import json
from models import User,House
from settings import db
user_page=Blueprint('user_page',__name__)
@user_page.route('/register',methods=['POST'])
def register():
    name=request.form['username']
    password=request.form['password']
    email=request.form['email']
    result=User.query.filter(User.name==name).all()
    if len(result)==0:
        user=User(name=name,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        json_str=json.dumps({'valid':'1','msg':user.name})
        res=Response(json_str)
        res.set_cookie('name',user.name,3600*2)
        return res
    else:
        return jsonify({'valid':'0','msg':'用户已注册!'})
    #用户中心展示路由
@user_page.route('/user/<name>',methods=['GET'])
def user(name):
    '''
    1.获取用户名。判断用户是否存在
    2.如果存在取出用户的所有id，把数据渲染到用户中心模板，3.如何不存在返回首页
    2.如果存在取出用户的所有数据（基本信息，收藏的房源信息对象，浏览房源对象）把数据渲染到用户中心模板
    '''
    user = User.query.filter(User.name == name).first()
    if user:
        #获取用户收藏记录的房源对象
        collect_id_str = user.collect_house_id
        if collect_id_str:#判断是否有收藏的房源
            collect_id_list = collect_id_str.split(',')
            collect_house_list = []#存储用户收藏房源的列表
            for hid in collect_id_list:
                house = House.query.get(int(hid))
                collect_house_list.append(house)
        else:#如果没有收藏记录返回空数据
            collect_house_list = []

        #获取用户浏览记录的房源对象
        seen_id_str = user.seen_id
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')
            seen_house_list=[]
            for hid in seen_id_list:
                house = House.query.get(int(hid))
                seen_house_list.append(house)
        else:
            seen_house_list = []
        return  render_template('user_page.html',user=user,collect_house_list=collect_house_list,seen_house_list=seen_house_list)
    else:
        return redirect('/')








@user_page.route('/login',methods=['POST'])
def login():
    name = request.form['username']
    password = request.form['password']

    user = User.query.filter(User.name==name).first()
    if user:
        if user.password == password:
            result = {'vaild':'1','msg':user.name }
            result_json = json.dumps(result)
            res = Response(result_json)
            res.set_cookie('name',user.name,3600*2)
            return res
        else:
            return jsonify({'valid':'0','msg':'密码不正确'})
    else:
        return  jsonify({'valid':'0','msg':'用户名不正确'})



@user_page.route('/logout')
def logout():
    name = request.cookies.get('name')
    if name:
        result = {'valid':'1','msg':'退出登录成功！'}
        json_str = json.dumps(result)
        res = Response(json_str)
        res.delete_cookie('name')
        return res
    else:
        return jsonify({'valid':'0','msg':'未登录'})





@user_page.route('/modify/userinfo/<option>',methods=['POST'])
def modify_info(option):
    if option == 'name':
        y_name = request.form['y_name']
        name = request.form['name']
        user = User.query.filter(User.name==y_name).first()
        other_user = User.query.filter(User.name == name).first()
        if user and not other_user:
            user.name = name
            db.session.commit()
            result = {'ok':'1'}
            json_str = json.dumps(result)
            #创建响应对象
            res = Response(json_str)
            res.set_cookie('name',User.name,3600*2)
            return res
        else:
            return jsonify({'ok','0'})
    elif option == 'addr':
        y_name = request.form['y_name']
        addr = request.form['addr']
        user = User.query.filter(User.name == y_name).first()
        if user:
            user.addr = addr
            db.session.commit()
            return jsonify({'ok','1'})
        else:
            return  jsonify({'ok','0'})
    elif option == 'password':
        y_name = request.form['y_name']
        password = request.form['password']
        user = User.query.filter(User.name == y_name).first()
        if user:
            user.password = password
            db.session.commit()
            return jsonify({'ok','1'})
        else:
            return jsonify({'ok','0'})
    elif option == 'email':
        y_name = request.form['y_name']
        email = request.form['email']
        user = User.query.filter(User.name == y_name).first()
        if user:
            user.email = email
            db.session.commit()
            return jsonify({'ok', '1'})
        else:
            return jsonify({'ok', '0'})
    return 'ok'



@user_page.route('add/collection/<int:hid>')
def add_collection_id(hid):
    name = request.cookies.get('name')
    if name:
        user = User.query.filter(User.name==name).first()
        collect_id_str = user.collect_house_id
        if collect_id_str:
            collect_id_list = collect_id_str.split(',')
            set_id = set([int(i) for i in collect_id_list])
            if hid in set_id:
                return jsonify({'valid':'1','msg':'已经收藏过了'})
            else:
                new_collect_id_str = collect_id_str+','+str(hid)
                user.collect_house_id = new_collect_id_str
                db.session.commit()
                return jsonify({'valid':'1','msg':'收藏完成'})

        else:
            user.collect_house_id=str(hid)
            db.session.commit()
            return jsonify({'valid':'1','msg':'收藏完成'})
    else:
        return jsonify({'valid':'0','msg':'登录后才能使用收藏功能'})


@user_page.route('/collect_off',methods=['POST'])
def collect_off():
    name = request.form['user_name']
    hid = request.form['house_id']
    user = User.query.filter(User.name == name).first()
    collect_id_str = user.collect_house_id
    collect_id_list = collect_id_str.split(',')
    if hid in collect_id_list:
        collect_id_list.remove(hid)
        new_collect_id_str = ','.join(collect_id_list)
        user.collect_house_id = new_collect_id_str
        db.session.commit()
        result = {'valid':'1','msg':'删除成功!'}
        return  jsonify(result)
    else:
        result = {'valid':'0','msg':'删除失败'}
        return jsonify(result)



@user_page.route('/del_record',methods=['POST'])
def del_record():
    name = request.form['user_name']
    user = User.query.filter(User.name==name).first()
    seen_id_str = user.seen_id
    if seen_id_str:
        user.seen_id=''
        db.session.commit()
        return jsonify({'valid':'1','msg':'删除成功'})
    else:
        return jsonify({'valid':'0','msg':'暂无信息可以删除'})





















