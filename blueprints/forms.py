import wtforms
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import Email,Length,EqualTo,InputRequired,Optional
from models import UserModel
from exts import db

class RegisterForm(wtforms.Form):
    email = wtforms.SearchField(validators=[Email(message="邮箱格式错误！")])
    # captcha = wtforms.SearchField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.SearchField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    # phone = wtforms.SearchField(validators=[Length(min=11, max=11, message="手机号码格式错误！")])
    password = wtforms.SearchField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.SearchField(validators=[EqualTo("password",message="两次密码不一致！")])

    # 验证邮箱是否已经被注册
    def validate_emil(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="邮箱已经被注册！")

    # # 验证验证码是否正确
    # def validate_captcha(self,field):
    #     captcha = field.data
    #     email = self.email.data
    #     captcha_model = EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
    #     if not captcha_model:
    #         raise wtforms.ValidationError(message="邮箱或者验证码错误！")
    #     # 可以删掉captcha_model
    #     else:
    #         db.session.delete(captcha)
    #         db.session.commit()

# 登录验证
class LoginForm(wtforms.Form):
    username = wtforms.SearchField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    email = wtforms.SearchField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.SearchField(validators=[Length(min=6, max=20, message="密码格式错误！")])

# 忘记密码验证
class ForgetForm(wtforms.Form):
    phone = wtforms.SearchField(validators=[Length(min=11, max=11, message="手机号码格式错误！")])
    username = wtforms.SearchField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    email = wtforms.SearchField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.SearchField(validators=[Length(min=6, max=20, message="密码格式错误！")])

# 二手物品发布验证
class ESObjectForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=1,max=100,message="标题格式错误！")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误！")])
    price = wtforms.StringField(validators=[Length(min=1, max=10, message="价格格式错误！")])
    # image = wtforms.FileField(validators=[FileRequired(), FileAllowed(["jpg", "png", "gif"],message="图片格式错误！")])

# 二手物品详情页评论验证
class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误！")])
    wuping_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id")])

# 二手物品详情页收藏验证
class FavoriteForm(wtforms.Form):
    wuping_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入物品id")])

# 修改账号信息验证
class UpdateForm(wtforms.Form):
    username = wtforms.SearchField(validators=[Length(min=3, max=20, message="用户名格式错误！"), Optional()])
    phone = wtforms.SearchField(validators=[Length(min=11, max=11, message="手机号码格式错误！"), Optional()])
    email = wtforms.SearchField(validators=[Email(message="邮箱格式错误！"), Optional()])
    citizen_id = wtforms.StringField(validators=[Length(min=18, max=18, message="身份证号码格式错误！"), Optional()])
    name = wtforms.StringField(validators=[Length(min=2, max=20, message="姓名格式错误！"), Optional()])

# 论坛发布验证
class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=2, max=100, message="标题格式错误！")])
    content = wtforms.StringField(validators=[Length(min=2, message="内容格式错误！")])

# 评论发布验证
class QaAnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=2, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id")])