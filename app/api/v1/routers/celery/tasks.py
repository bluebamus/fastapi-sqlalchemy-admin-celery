import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # root 경로 추가

from main import celery_app


@celery_app.task
def crawling():
    return "crawling"


@celery_app.task
def warmup():
    return "ready"


@celery_app.task
def divide(x, y):
    import time

    time.sleep(5)
    return x / y
