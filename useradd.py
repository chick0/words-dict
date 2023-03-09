from os import environ

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import User

if "SQLALCHEMY_DATABASE_URI" not in environ:
    load_dotenv()

SQLALCHEMY_DATABASE_URI = environ['SQLALCHEMY_DATABASE_URI']

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    pool_size=1,
    max_overflow=2
)

factory = sessionmaker(bind=engine)


def main():
    discord_id = input("데이터베이스에 추가할 계정의 디스코드 아이디를 입력해주세요. : ")

    session = factory()

    user: User = session.query(User).filter_by(
        discord_id=discord_id
    ).first()

    if user is not None:
        print("이미 등록된 계정입니다.")
        return

    user = User()
    user.discord_id = discord_id

    session.add(user)
    session.commit()
    session.close()
    print("사용자가 등록되었습니다. 해당 사용자의 로그인 이후 계정 정보 설정이 완료됩니다.")


if __name__ == "__main__":
    main()
