from flask import Blueprint,render_template,request, jsonify, redirect, url_for, session, g, send_file
from decorators import login_required
from exts import db
from models import UserModel, UserDetailModel, AreaModel, AddressModel
from blueprints.forms import UpdateForm
import tempfile

bp = Blueprint('usercenter', __name__, url_prefix='/usercenter')

# 基本信息
@bp.route('/basic', methods=['GET', 'POST'])
@login_required
def basic():
    if request.method == 'GET':
        user_detail = UserDetailModel.query.filter_by(user_id=g.user.id).first()
        provinces = AreaModel.query.filter_by(parent_id=0).all()
        return render_template('个人中心页面/个人中心-基本信息.html', user_detail=user_detail, provinces=provinces)
    else:
        user_detail = UserDetailModel.query.filter_by(user_id=g.user.id).first()
        if 'head_photo' in request.files:
            file = request.files['head_photo']
            img_stream = file.read()
            user_detail.head_photo = img_stream
            db.session.commit()
            return redirect(url_for('usercenter.basic'))
        if request.form:
            form = request.form
            user_detail.nickname = form['nickname']
            db.session.commit()
            return redirect(url_for('usercenter.basic'))
        
        return redirect(url_for('usercenter.basic'))

# 更新基本信息
@bp.route('/update_basic', methods=['POST'])
def update_basic():
    data = request.get_json()
    if data:
        user_detail = UserDetailModel.query.filter_by(user_id=g.user.id).first()
        if data.get('nickname'):
            user_detail.nickname = data.get('nickname')
        if data.get('sex'):
            user_detail.sex = data.get('sex')
        if data.get('city'):
            user_detail.city = data.get('city')
        if data.get('aboutme'):
            user_detail.Personal_signature = data.get('aboutme')
        db.session.commit()
        return 'successfully'
    else:
        return jsonify({"data": data})

# 返回头像
@bp.route('/head_photo', methods=['GET'])
@login_required
def head_photo():
    user_detail = UserDetailModel.query.filter_by(user_id=g.user.id).first()
    if user_detail:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(user_detail.head_photo)
            temp_file.flush()
            return send_file(temp_file.name, mimetype='image/jpeg')
    else:
        return send_file('static/source/八度空间.jpg', mimetype='image/jpeg')

# 账户信息
@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'GET':
        user_detail = UserDetailModel.query.filter_by(user_id=g.user.id).first()
        return render_template('个人中心页面/个人中心-账号信息.html', user=g.user, user_detail=user_detail)
    else:
        user = UserModel.query.filter_by(id=g.user.id).first()
        user_detail = UserDetailModel.query.filter_by(user_id=g.user.id).first()
        form = UpdateForm(request.form)
        if form.validate():
            if form.username.data:
                user.username = form.username.data
            if form.phone.data:
                user_detail.phone = form.phone.data
            if form.citizen_id.data:
                user_detail.citizen_id = form.citizen_id.data
            if form.name.data:
                user_detail.name = form.name.data
            if form.email.data:
                user.email = form.email.data
            db.session.commit()
            return redirect(url_for('usercenter.account'))
        else:
            return jsonify(form.errors)

# 收货地址
@bp.route('/address', methods=['GET', 'POST'])
@login_required
def address():
    if request.method == 'GET':
        addresses = AddressModel.query.filter_by(user_id=g.user.id).all()
        provinces = AreaModel.query.filter_by(parent_id=0).all()
        return render_template('个人中心页面/个人中心-收货地址.html', provinces=provinces, addresses=addresses)
    
# 获取城市
@bp.route('/cities')
def get_cities():
    province_id = request.args.get('province_id')  # 获取前端传递的省份id
    if not province_id:
        return ''  # 如果没有选择省份，则返回空字符串
    else:
        cities = AreaModel.query.filter_by(parent_id=province_id).all()
        # 将城市列表转换成字典形式，方便序列化到 JSON 格式
        cities_dict = [{'name': city.name, 'id': city.area_id} for city in cities]
        return jsonify(cities=cities_dict)

# 获取区县
@bp.route('/districts')
def get_areas():
    city_id = request.args.get('city_id')  # 获取前端传递的城市id
    if not city_id:
        return ''  # 如果没有选择城市，则返回空字符串
    else:
        districts = AreaModel.query.filter_by(parent_id=city_id).all()
        # 将区县列表转换成字典形式，方便序列化到 JSON 格式
        districts_dict = [{'name': district.name, 'id': district.area_id} for district in districts]
        return jsonify(districts=districts_dict)
    
# 保存地址
@bp.route('/save_address', methods=['POST'])
def save_address():
    data = request.get_json()
    if data:
        address = AddressModel(user_id=g.user.id, person=data.get('contactPerson'), address=data.get('address'), phone=data.get('phone'), type=data.get('addressType'))
        db.session.add(address)
        db.session.commit()
        return 'Address saved successfully'

# 设为默认地址
@bp.route('/set_default', methods=['POST'])
def set_default():
    data = request.get_json()
    if data:
        print(data.get('addressId'))
        addresses = AddressModel.query.filter_by(user_id=data.get('userId')).all()
        for address in addresses:
            address.default_address = False
            if address.id == data.get('addressId'):
                address.default_address = True
        
        db.session.commit()
        return 'Address set as default successfully'
    else:
        return jsonify({"data": data})
    

# 删除地址
@bp.route('/delete_address', methods=['POST'])
def delete_address():
    data = request.get_json()
    if data:
        address = AddressModel.query.filter_by(id=data.get('addressId')).first()
        db.session.delete(address)
        db.session.commit()
        return 'Address deleted successfully'
    else:
        return jsonify({"data": data})