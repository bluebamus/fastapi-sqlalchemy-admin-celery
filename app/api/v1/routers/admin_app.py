from fastapi import FastAPI
from sqladmin import Admin
from app.core.database import engine
from app.core.settings import ENV_PATH, settings
from app.api.v1.routers.user.user_admin import UserAdmin, UserProfileAdmin, GroupAdmin
from app.api.v1.routers.blog.blog_admin import PostAdmin
from app.api.v1.routers.celery.celery_admin import (
    CeleryTaskAdmin,
    CeleryBeatIntervalScheduleAdmin,
    CeleryBeatClockedScheduleAdmin,
    CeleryBeatCrontabScheduleAdmin,
    CeleryBeatSolarScheduleAdmin,
    CeleryBeatPeriodicTaskChangedEventAdmin,
    CeleryBeatPeriodicTaskAdmin,
)


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
    admin.add_view(CeleryTaskAdmin)
    admin.add_view(CeleryBeatIntervalScheduleAdmin)
    admin.add_view(CeleryBeatClockedScheduleAdmin)
    admin.add_view(CeleryBeatCrontabScheduleAdmin)
    admin.add_view(CeleryBeatSolarScheduleAdmin)
    admin.add_view(CeleryBeatPeriodicTaskChangedEventAdmin)
    admin.add_view(CeleryBeatPeriodicTaskAdmin)

    return admin

    