from exts import db
from datetime import datetime

# 用户信息数据库
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    # phone = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

# 二手物品发布信息
class ESObjectModel(db.Model):
    __tablename__ = "esobject"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(10), nullable=False)
    creat_time = db.Column(db.DateTime,default=datetime.now)
    image = db.Column(db.LargeBinary)
    # 外键
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    # 关系
    author = db.relationship(UserModel,backref="wuping")

# 收藏物品数据库
class FavoriteObjectModel(db.Model):
    __tablename__ = "user_favorite"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    wuping_id = db.Column(db.Integer,db.ForeignKey("esobject.id"))
    # 关系
    user = db.relationship(UserModel, backref="user_favorite")
    wuping = db.relationship(ESObjectModel,backref=db.backref("favorite",order_by=creat_time.desc()))


# 评论数据库
class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    # 外键
    wuping_id = db.Column(db.Integer,db.ForeignKey("esobject.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 关系
    wuping = db.relationship(ESObjectModel,backref=db.backref("answers",order_by=creat_time.desc()))
    author = db.relationship(UserModel,backref="answers")

# 用户详细信息数据库
class UserDetailModel(db.Model):
    __tablename__ = "user_detail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 关系
    user = db.relationship(UserModel,backref="user_detail")

    nickname = db.Column(db.String(64), nullable=True)  # 昵称
    city = db.Column(db.String(64), nullable=True)  # 城市
    sex = db.Column(db.String(5), nullable=True)  # 性别
    Personal_signature = db.Column(db.String(128), nullable=True)  # 个性签名
    head_photo = db.Column(db.LargeBinary, nullable=True)   # 头像

    phone = db.Column(db.String(11), nullable=True) # 手机号

    citizen_id = db.Column(db.String(18), nullable=True) # 身份证号
    name = db.Column(db.String(32), nullable=True)  # 姓名

# 地区数据库
class AreaModel(db.Model):
    __tablename__ = "dou_area"
    area_id = db.Column(db.SmallInteger, primary_key=True)
    parent_id = db.Column(db.SmallInteger, nullable=False)
    name = db.Column(db.String(120), nullable=False)

# 收货地址数据库
class AddressModel(db.Model):
    __tablename__ = "address"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(64), nullable=False) # 收货人
    phone = db.Column(db.String(11), nullable=False)    # 手机号
    address = db.Column(db.String(256), nullable=False) # 收货地址
    default_address = db.Column(db.Boolean, default=False) # 默认地址标识
    type = db.Column(db.String(16), nullable=False) # 收货地址类型
    # 关系
    user = db.relationship(UserModel,backref="address")

# 论坛数据库
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 关系
    author = db.relationship(UserModel, backref="questions")

# 论坛评论数据库
class QaAnswerModel(db.Model):
    __tablename__ = "qa_answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    question = db.relationship(QuestionModel,backref=db.backref("answers",order_by=creat_time.desc()))
    author = db.relationship(UserModel,backref="qa_answers")



# 邮箱验证码数据库
# class EmailCaptchaModel(db.Model):
#     __tablename__ = "emali_captcha"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(100), nullable=False)
#     captcha = db.Column(db.String(100), nullable=False)
#     # tage = db.Column(db.Boolean,default=False)  可以用来判断验证码是否被使用了

