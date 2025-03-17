from fastapi import FastAPI
from app.core.settings import ENV_PATH, settings
from app.api.v1.routers.admin_app import init_admin
from app.core.database import engine
from app.core.database import Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

init_admin(app, engine)

Base.metadata.create_all(engine)  # Create tables

# admin = Admin(
#     app,
#     engine,
#     base_url=settings.ADMIN_BASE_URL,
# )


# admin.add_view(UserAdmin)
