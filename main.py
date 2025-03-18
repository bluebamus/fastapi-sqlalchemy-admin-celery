from fastapi import FastAPI
from app.core.settings import ENV_PATH, settings
from app.api.v1.routers.admin_app import init_admin
from app.core.database import engine
from app.core.database import Base
from app.core.middleware import CustomCORSMiddleware

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


celery = Celery(
    # __name__,
    "Client Publisher App",
    broker="redis://127.0.0.1:6379/0",
    backend="db+sqlite:///./test.db",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@celery.task
def divide(x, y):
    import time

    time.sleep(5)
    return x / y


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
