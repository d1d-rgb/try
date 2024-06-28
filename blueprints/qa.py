#-*- codeing = utf-8 -*-
#@Time : 2023/12/9 16:21
from flask import Blueprint,render_template,request, jsonify, redirect, url_for, session,g,Flask
from exts import db
from models import QuestionModel,QaAnswerModel
from .forms import QuestionForm,QaAnswerForm
from decorators import login_required
bp=Blueprint("qa",__name__,url_prefix="/qa")

# 论坛主页面
@bp.route("/main")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.creat_time.desc()).all()
    return render_template("论坛/论坛首页.html",questions=questions)

# 论坛帖子发布
@bp.route("/public",methods=['GET','POST'])
@login_required
def public_question():
    if request.method == 'GET':
        print("000")
        return render_template("论坛/发布.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            print(title)
            return redirect(url_for("qa.index"))
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

# 论坛详情页面
@bp.route("/detail/<qa_id>")
@login_required
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("论坛/帖子详情.html", question=question)

# 论坛评论
@bp.route("/public_answer", methods=['POST'])
def public_answer():
    form = QaAnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = QaAnswerModel(content=content,question_id=question_id,author_id=g.user.id)  #
        print("评论成功！")
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        print("评论失败!")
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))

# 论坛搜索
@bp.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("论坛/搜索帖子.html",questions = questions)

# 热门论坛
@bp.route("/hot_posts")
def hot_posts():
    hot_questions = QuestionModel.query.outerjoin(QaAnswerModel).group_by(QuestionModel.id).order_by(db.func.count(QaAnswerModel.id).desc()).all()
    is_hot_page = True  # 设置is_hot_page变量为True
    return render_template("论坛/论坛首页.html", hot_questions=hot_questions, is_hot_page=is_hot_page)


