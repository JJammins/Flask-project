from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
# wtfroms.validators : 유효성 검증 관련 모듈
# Datarequired : 이 필드는 반드시 값을 써야하는 필드임
# Email : 이메일 형식을 반드시 지켜야 하는 필드 ~~@~~.~
# length : 입력한 값의 길이 관련 

# 사용자 신규 작성과 사용자 편집 폼 클래스
class UserForm(FlaskForm):
    # 사용자폼의 username 속성의 라벨과 검증 설정
    username = StringField(
        "사용자명",
        validators=[
            DataRequired(message="사용자명은 필수입니다."),
            Length(max=30, message="30문자 이내로 입력해주세요."),
        ],
    )
    # 사용자폼 email 속성의 라벨과 검증 설정
    email = StringField(
        "메일 주소",
        validators=[
            DataRequired(message="메일 주소는 필수입니다."),
            Email(message="메일 주소의 형식으로 입력해주세요."),
        ],
    )
    # 사용자폼 password 속성의 라벨과 검증 설정
    password = PasswordField(
        "비밀번호",
        validators=[DataRequired(message="비밀번호는 필수입니다.")]
    )
    # 사용자폼 submit의 문구를 설정한다
    submit = SubmitField("신규 등록")