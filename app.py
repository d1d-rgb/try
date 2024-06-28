from flask import Flask,session,g,render_template,send_from_directory
import os
import config
from exts import db,mail
from models import UserModel
from blueprints.users import bp as users_bp
from blueprints.wuping import bp as wuping_bp
from blueprints.userCener import bp as useercenter_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定配置文件config.py
app.config.from_object(config)
# 绑定db,mail
db.init_app(app)
mail.init_app(app)
# 映射到数据库中
migrate = Migrate(app,db)
# 绑定user_bp
app.register_blueprint(users_bp)
# 绑定wuping_bp
app.register_blueprint(wuping_bp)
# 绑定useercenter_bp
app.register_blueprint(useercenter_bp)
# 绑定qa_bp
app.register_blueprint(qa_bp)

# 在请求前获取用户名称
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

# 联系上下文，使得后续可以获取到用户名m
@app.context_processor
def my_context_processor():
    return {"user": g.user}



if __name__ == '__main__':
    app.run(debug=True)
