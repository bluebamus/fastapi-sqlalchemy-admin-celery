from starlette.requests import Request
from typing import Any
from sqlalchemy import DateTime
from sqladmin import ModelView
from app.models.model import Post


class PostAdmin(ModelView, model=Post):
    pass
