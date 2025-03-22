# CryptContext는 여러 해싱 알고리즘을 지원하고, 여기서는 bcrypt를 사용
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    """
    비밀번호를 해싱하여 반환
    :param password: 사용자 입력 비밀번호
    :return: 해싱된 비밀번호
    """
    return pwd_context.hash(password)


def check_password_hash(hashed_password: str, password: str) -> bool:
    """
    사용자가 입력한 비밀번호가 저장된 해시와 일치하는지 확인
    :param hashed_password: 저장된 해시된 비밀번호
    :param password: 사용자가 입력한 비밀번호
    :return: 비밀번호가 일치하면 True, 아니면 False
    """
    return pwd_context.verify(password, hashed_password)
