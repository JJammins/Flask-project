from email_validator import validate_email, EmailNotValidError
# from flask_debugtoolbar import DebugToolbarExtension
from flask import ( Flask,
                   render_template,
                   url_for,
                   request,
                   redirect,
                   flash )
import logging
import os
from flask_mail import Mail, Message


# 서버 프로그램 객체를 만든다.
# __name__ : 실행 중인 모듈의 시스템 상의 이름
app = Flask(__name__)

# SECRET_KEY 추가
app.config["SECRET_KEY"] = "1998Sus5DNJF27Dlf"

# Mail 클래스의 config를 추가
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록
mail = Mail(app)

# 로그 레벨 설정
app.logger.setLevel(logging.DEBUG)

# 리다이렉트를 중단하지 않도록 한다
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtension에 애플리케이션을 설정한다
# toolbar = DebugToolbarExtension(app)

# 기본 주소로 요청이 왔을 때 무엇을 할지 정의하기
@app.route("/")
def index():
    return "Hello, Flask"

# 기본 주소 뒤에 /hello 를 적었을 때 나타나는 화면
@app.route("/hello")
def hello():
    return "Hello, World!"

# 메소드에 따른 처리를 원한다면 구별해서 정의할 수 있다
# 엔드포인트명을 지정하지 않으면 함수명이 엔드포인트명이된다
@app.route("/hello/<name>",
           methods=["GET"],
           endpoint="hello-endpoint")
def hello(name):
    return f'Hello, {name}!!'

# show_name 엔드포인트 작성
@app.route("/name/<name>")
def show_name(name):
    # 변수를 템플릿 엔진에게 건넨다
    return render_template("index.html", name=name)

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world/
    print(url_for("hello-endpoint", name="world"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="1"))

# p.62 폼 만들기 : 엔드포인트 추가하기
# 문의 폼 화면을 반환하는 contact 엔드포인트를 만듬
# http://127.0.0.1:5000/contact
# 플라스크의 템플릿 문서는 앱 내 templates폴더에 있다고 가정한다
@app.route("/contact")
def contact():
    return render_template("contact.html") # GET

# view
# http://127.0.0.1:5000/contact/complete
# post 요청이 오면 필요한 데이터 관련 처리를 하고나서
# contact_complete.html 템플릿을 주는 get 처리를 하면서 마무리
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    # request.method 속성을 이용하여 요청된 메서드를 확인
    if request.method == "POST":
        # form 속성을 사용해서 폼의 값을 취득한다
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        print(username, email, description)

        # 유효성 검사 파트
        is_valid = True
        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False
        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False
        try:
            validate_email(email) # 이메일 형식 검사
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False
        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False
        if not is_valid:
            return redirect(url_for("contact"))
        
        # 이메일을 보낸다
        send_email(
            email, # 이메일 주소
            "문의 감사합니다.", # 이메일 제목
            "contact_mail", # 이메일의 내용의 템플릿
            username=username, # 사용자명
            description=description, # 문의 내용
        )

        # contact 엔드포인트로 리다이렉트한다
        flash("문의해 주셔서 감사합니다")
        return redirect(url_for("contact_complete", username=username, email=email, description=description))
    
    return render_template("contact_complete.html")

# 이메일 보내기 위해서 API 사용하는 함수
def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)