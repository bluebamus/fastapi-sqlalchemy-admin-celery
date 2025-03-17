from starlette.requests import Request
from typing import Any
from sqlalchemy import DateTime
from sqladmin import ModelView
from app.models.model import Post


class PostAdmin(ModelView, model=Post):
    name = "포스트"
    name_plural = "포스트 목록"
    icon = "fa-solid fa-user"
    category = "포스트 관리"

    form_columns = [
        Post.user_id,
        Post.title,
        Post.content,
        Post.is_published,
        Post.user_posts,
    ]

    form_ajax_refs = {
        "user_posts": {
            "fields": ["username", "email"],  # 검색 가능 필드
            "order_by": "username",  # 정렬 방식
            "page_size": 20,  # 한 번에 표시할 사용자 수
        }
    }
