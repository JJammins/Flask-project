from flask import Blueprint, render_template, redirect, url_for
from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm

# Blueprint로 crud앱을 생성한다
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# index 엔드포인트를 작성하고 index.html을 반환
@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
#     user = User(
#         username="김재민",
#         email="holic3410@naver.com",
#         password="19192929"
#     )
    # db.session.add(user)
    # db.session.commit()
    # user = db.session.query(User).filter_by(id=1).delete()
    # db.session.commit()
    # db.session.query(User).all() # 모든 데이터 가져오기
    # db.session.query(User).first() # 데이터 1건 가져오기 (첫번째 레코드 가져옴)
    # db.session.query(User).get(2) # 기본 키가 2인 레코드 가져오기
    # db.session.query(User).count() # 레코드 개수 가져오기
    # # paginate(page=None, per_page=None, error_out=True, max_per_page=None)
    # # db.session.query(User).paginate(2, 10, False)
    # db.session.query(User).filter_by(id=2, username="admin").all() # id가 2이고 username이 admin인 레코드 가져오기
    # db.session.query(User).filter(User.id==2, User.username=="admin").all() # id가 2이고 username이 admin인 레코드 가져오기
    # db.session.query(User).limit(1).all() # 가져올 레코드의 개수를 1건으로 지정하기
    # db.session.query(User).limit(1).offset(2).all() # 3번째의 레코드로부터 1건 가져오기
    # db.session.query(User).order_by("username").all() # username을 정렬
    # db.session.query(User).group_by("username").all() # username을 그룹화
    return "콘솔 로그를 확인해 주세요"

@crud.route("/users/new",
            methods = ["GET", "POST"])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
def users():
    """사용자의 일람을 취득한다"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>",
            methods=["GET", "POST"],)
def edit_user(user_id):
    form = UserForm()
    # User 모델을 이용하여 사용자 취득
    user = User.query.filter_by(id=user_id).first()
    # from으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람 화면으로 리다이렉트
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    # GET의 경우는 html을 반환
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))