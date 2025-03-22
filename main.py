from fastapi import FastAPI
from app.core.settings import ENV_PATH, settings
from app.api.v1.routers.admin_app import init_admin
from app.core.database import engine, Base, get_db
from app.core.middleware import CustomCORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from celery import Celery

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

init_admin(app, engine)

Base.metadata.create_all(engine)  # Create tables

# Create an instance of your custom CORS middleware
custom_cors_middleware = CustomCORSMiddleware(app)

# Configure CORS middleware based on environment
custom_cors_middleware.configure_cors()


celery_app = Celery(
    # __name__,
    "Client Publisher App",
    include=[
        "app.api.v1.routers.celery.tasks",
    ],
    # broker=settings.CELERY_BROKER,
    # backend=settings.CELERY_BACKEND,
)

celery_app.config_from_object("app.core.celeryconfig")

# celery_app = Celery(
#     # __name__,
#     "Client Publisher App",
#     broker=settings.CELERY_BROKER,
#     backend=settings.CELERY_BACKEND,
# )

# beat_dburi = "sqlite:///./test.db"
# MySQL: `pip install mysql-connector`
# beat_dburi = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/celery-schedule'
# # PostgreSQL: `pip install psycopg2`
# beat_dburi = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/celery-schedule'

# celery_app.conf.update(
#     {
#         "beat_dburi": settings.CELERY_BEAT_DB_URL,
#         "beat_schema": None,  # you can make the scheduler tables under different schema (tested for postgresql, not available in sqlite)
#     }
# )

# celery_app.conf.imports = [
#     "app.api.v1.routers.celery.tasks",
# ]


# @app.get("/")
# async def root():
#     warmup.delay()


# 테스트를 위한 라우트 추가
@app.get("/test-cors")
async def test_cors():
    # CORS가 올바르게 설정되었는지 확인하는 예시 코드
    # 이 엔드포인트는 CORS 헤더를 확인하고 적절한 응답을 반환합니다.
    if settings.ENVIRONMENT == "development":
        allowed_origins = settings.CORS_ALLOW_ORIGINS
    else:
        allowed_origins = ["*"]

    return {
        "message": "CORS 설정이 올바르게 적용되었습니다.",
        "allowed_origins": allowed_origins,
    }
