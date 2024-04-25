from pathlib import Path # 경로 처리를 위한 기본 라이브러리
from flask import Flask 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect # 폼의 확장 기능 import

db = SQLAlchemy()
csrf = CSRFProtect() # 폼의 확장기능 인스턴스화
def create_app() :

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="sksms12qkqh34dpdy",
        SQLALCHEMY_DATABASE_URI=
        f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQL을 콘솔 로그에 출력하는 설정
        SQLALCHEMY_ECHO=True,
    
        WTF_CSRF_SECRET_KEY="AuwyszU5sugKN7KZs6f" # 폼의 확장 기능 관련 시크릿키
    )

    # 앱과 연계
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app