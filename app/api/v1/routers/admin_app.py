from fastapi import FastAPI
from sqladmin import Admin
from app.core.database import engine
from app.core.settings import ENV_PATH, settings
from app.api.v1.routers.user.user_admin import UserAdmin, UserProfileAdmin, GroupAdmin
from app.api.v1.routers.blog.blog_admin import PostAdmin


def init_admin(
    app: FastAPI,
    db_engine: engine,
    base_url: str = "/admin",
) -> Admin:
    admin = Admin(
        app,
        db_engine,
        base_url=settings.ADMIN_BASE_URL,
    )

    admin.add_view(UserAdmin)
    admin.add_view(UserProfileAdmin)
    admin.add_view(GroupAdmin)
    admin.add_view(PostAdmin)
    return admin
