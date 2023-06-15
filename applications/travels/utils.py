import random
import string
from datetime import datetime


def check_date_order(start_date, end_date):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    if start_dt <= end_dt:
        return True
    else:
        return False


def generate_random_string(length):
    """랜덤 문자열 생성 함수"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
