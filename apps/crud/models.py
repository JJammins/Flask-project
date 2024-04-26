from datetime import datetime

from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    # primary_key : 이 데이터를 상징하는, 식별값 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 속성값 getter
    @property
    def password(self):
        raise AttributeError("읽어들일 수 없음")

    # 속성값 setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 비밀번호 체크
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # 이메일 중복 체크
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None
    
# 로그인하고 있는 사용자 정보를 취득하는 함수
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)