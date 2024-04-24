from flask import Flask

# create_app() 함수 작성
def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # crud 패키지로부터 views를 import 한다
    from apps.crud import views as crud_views

    # register_blueprint를 사용해 views의 curd를 앱에 등록
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app