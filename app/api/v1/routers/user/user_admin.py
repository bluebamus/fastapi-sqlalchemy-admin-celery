from starlette.requests import Request
from typing import Any
from sqlalchemy import DateTime
from sqladmin import ModelView
from app.models.model import User, UserProfile, Group
from app.utils.authentication import generate_password_hash, check_password_hash


class UserProfileAdmin(ModelView, model=UserProfile):
    name = "사용자 프로필"
    name_plural = "사용자 프로필 목록"
    icon = "fa-solid fa-user"
    category = "사용자 관리"

    column_list = [UserProfile.id, UserProfile.full_name, "user.username"]

    # form에 표시할 필드
    form_columns = [
        UserProfile.user,  # 직접 user_id를 선택하도록 함
        UserProfile.full_name,
        UserProfile.bio,
        UserProfile.avatar_url,
        UserProfile.phone_number,
        UserProfile.address,
    ]

    column_searchable_list = (
        UserProfile.id,
        UserProfile.full_name,
    )

    column_sortable_list = (
        UserProfile.id,
        UserProfile.full_name,
        # User.email,
    )

    column_sortable_list = (UserProfile.id, UserProfile.full_name)
    column_default_sort = (UserProfile.id, True)

    # 디테일 페이지에서 외래 키 선택 시 보여줄 레이블 설정
    # 사용자를 검색해서 고르는 방식
    form_ajax_refs = {
        "user": {
            "fields": ["username", "email"],  # 검색 가능 필드
            "order_by": "username",  # 정렬 방식
            "page_size": 20,  # 한 번에 표시할 사용자 수
        }
    }

    def __str__(self) -> str:
        return self.username


class GroupAdmin(ModelView, model=Group):
    name = "사용자 그룹"
    name_plural = "사용자 그룹 목록"
    icon = "fa-solid fa-user"
    category = "사용자 관리"

    form_columns = [
        Group.name,
        Group.description,
        Group.is_public,
        Group.user_group,
    ]


class UserAdmin(ModelView, model=User):
    # sqlalchemy admin을 사용하기 위해서는 lazy 모드를 사용하면 안된다. 에러가 발생한다.

    """
    can_create: 모델이 SQLAdmin을 통해 새 인스턴스를 생성할 수 있는지 여부입니다. 기본값은 True입니다.
    can_edit: 모델 인스턴스를 SQLAdmin을 통해 수정할 수 있는지 여부입니다. 기본값은 True입니다.
    can_delete: 모델 인스턴스를 SQLAdmin을 통해 삭제할 수 있는지 여부입니다. 기본값은 True입니다.
    can_view_details: 모델 인스턴스의 세부 정보를 SQLAdmin을 통해 볼 수 있는지 여부입니다. 기본값은 True입니다.
    """

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    action_disallowed_list = []

    """
    name: 이 모델의 표시 이름입니다. 기본값은 클래스 이름입니다.
    name_plural: 이 모델의 복수형 표시 이름입니다. 기본값은 클래스 이름 + s입니다.
    icon: 관리자에서 이 모델에 표시할 아이콘입니다. FontAwesome와 Tabler 이름만 지원됩니다.
    category: 드롭다운 메뉴에서 ModelView 클래스 그룹을 함께 표시할 카테고리 이름입니다.

    """
    name = "사용자"
    name_plural = "사용자 목록"
    icon = "fa-solid fa-user"
    category = "사용자 관리"

    """
    column_list: 목록 페이지에 표시할 열이나 열 이름의 리스트입니다.
    column_exclude_list: 목록 페이지에서 제외할 열이나 열 이름의 리스트입니다.
    column_formatters: 목록 페이지의 열 형식 지정기의 사전입니다.
    column_searchable_list: 목록 페이지에서 검색 가능한 열이나 열 이름의 리스트입니다.
    column_sortable_list: 목록 페이지에서 정렬 가능한 열이나 열 이름의 리스트입니다.
    column_default_sort: 정렬이 적용되지 않았을 때의 기본 정렬입니다. (열, 내림차순 여부)의 튜플 또는 여러 열에 대한 튜플의 리스트입니다.
    list_query: 목록 쿼리를 사용자 정의할 수 있는 메서드입니다. (request) -> stmt 형식을 따릅니다.
    count_query: 카운트 쿼리를 사용자 정의할 수 있는 메서드입니다. (request) -> stmt 형식을 따릅니다.
    search_query: 검색 쿼리를 사용자 정의할 수 있는 메서드입니다. (stmt, term) -> stmt 형식을 따릅니다.

    특정한 모든 열을 수동으로 지정하지 않고도 column_list나 column_details_list에서 "all" 특수 키워드를 사용할 수 있습니다. 예를 들어: column_list = "all"
    """

    # 목록 화면에서 표시할 모델 필드를 지정
    # 모델 필드명을 문자열로 지정하는 게 아니라, 모델의 필드를 직접 전달해서 직관적
    column_list = (
        User.id,
        User.username,
        User.is_active,
    )

    # 검색할 때 검색 대상이 되는 모델 필드를 지정
    # 기본적으로 검색어를 포함하는지(contains) 여부로 검색
    column_searchable_list = (
        User.id,
        User.username,
    )

    #  정렬할 수 있는 모델 필드를 지정
    column_sortable_list = (
        User.id,
        User.username,
        # User.email,
    )

    # column_default_sort 는 정렬을 따로 지정하지 않으면 기본으로 정렬할 모델 필드를 가리키는데,
    # 두 번째 값( True )은 역순으로 할 것인지 여부를 지정
    # (User.id, True) 는 id 모델 필드에 대해 역순으로 정렬하겠다는 뜻

    """
    상세 페이지
    이 옵션들은 단일 User의 세부 정보를 볼 수 있는 상세 페이지(Details page) 설정을 구성하는 데 사용됩니다.

    사용 가능한 옵션은 다음과 같습니다:

    column_details_list:    상세 페이지에서 표시할 컬럼 또는 컬럼 이름들의 리스트입니다.
    column_details_exclude_list:    상세 페이지에서 제외할 컬럼 또는 컬럼 이름들의 리스트입니다.
    column_formatters_detail:    상세 페이지에서 컬럼의 형식을 지정하는 딕셔너리입니다.
    """

    # column_details_list = [
    #     User.id,
    #     User.username,
    #     User.hashed_password,
    #     User.age_level,
    #     User.is_active,
    # ]

    # column_details_exclude_list = [
    #     User.created_at,
    # ]

    column_default_sort = (User.id, True)

    column_formatters = {User.username: lambda m, a: m.username[:10]}

    """
    폼 옵션 (Form options)
    SQLAdmin은 모델과 함께 동작하는 폼을 사용자 정의할 수 있도록 지원합니다.
    SQLAdmin의 폼은 WTForms 패키지를 기반으로 하며, 다음과 같은 옵션을 포함합니다.

    form: 모델을 생성하거나 수정할 때 사용할 기본 폼. 기본값은 None이며, 폼은 동적으로 생성됩니다.
    form_base_class: 폼을 생성할 때 사용할 기본 클래스. 기본값은 wtforms.Form입니다.
    form_args: WTForms에서 지원하는 폼 필드의 인자(Dictionary).
    form_widget_args: WTForms에서 지원하는 위젯 렌더링 인자(Dictionary).
    form_columns: 폼에 포함할 모델 컬럼 목록. 기본적으로 모든 모델 컬럼이 포함됩니다.
    form_excluded_columns: 폼에서 제외할 모델 컬럼 목록.
    form_overrides: 폼을 생성할 때 특정 필드를 재정의하는 Dictionary.
    form_include_pk: 기본 키(Primary Key) 컬럼을 생성/수정 폼에 포함할지 여부. 기본값은 False.
    form_ajax_refs: Select2를 사용하여 관계(Relationship) 모델을 비동기적으로 불러오도록 설정. 관련 모델에 많은 레코드가 있을 때 유용함.
    form_converter: 추가적인 컬럼 타입을 지원하도록 사용자 정의 변환기(Converter)를 추가할 수 있음.
    form_edit_query: (request) -> stmt 형태의 메서드를 사용하여 수정 폼 데이터를 커스터마이징할 수 있음.
    form_rules: 폼의 렌더링 및 동작을 관리하는 규칙 목록.
    form_create_rules: 생성(Create) 페이지에서 폼의 렌더링 및 동작을 관리하는 규칙 목록.
    form_edit_rules: 수정(Edit) 페이지에서 폼의 렌더링 및 동작을 관리하는 규칙 목록.

    form_columns = [User.name]
    form_args = dict(name=dict(label="Full name"))
    form_widget_args = dict(email=dict(readonly=True))
    form_overrides = dict(email=wtforms.EmailField)
    form_include_pk = True
    form_ajax_refs = {
        "address": {
            "fields": ("zip_code", "street"),
            "order_by": ("id",),
        }
    }
    form_create_rules = ["name", "password"]
    form_edit_rules = ["name"]
    """

    form_columns = (
        "username",
        "email",
        "age_level",
        "hashed_password",
        "is_active",
    )

    """
    page_size: 페이지네이션의 기본 페이지 크기입니다. 기본값은 10입니다.
    page_size_options: 페이지네이션 선택기 옵션입니다. 기본값은 [10, 25, 50, 100]입니다.
    """
    # 한 페이지에 몇 개 항목이 나오는지 지정
    page_size = 50
    page_size_options = [25, 50, 100, 200]

    """
    다음은 목록 페이지와 세부 페이지 모두에 적용되는 몇 가지 옵션이 있습니다.

    column_labels: 컬럼 레이블 매핑으로, 모든 곳에서 컬럼 이름을 새 이름으로 매핑하는 데 사용됩니다.
    column_type_formatters: 모든 곳에서 형식을 지정하기 위한 타입 키와 호출 가능한 값의 매핑입니다. 예를 들어, 목록 페이지와 상세 페이지 모두에서 사용할 사용자 지정 날짜 포맷터를 추가할 수 있습니다.
    save_as: 객체 편집 시 "새로 저장" 옵션을 활성화하는 불리언 값입니다.
    save_as_continue: save_as가 활성화된 경우 리디렉션 URL을 제어하는 불리언 값입니다.

    save_as 옵션
        save_as 옵션은 기존 객체를 편집할 때 해당 객체의 복사본을 새로운 객체로 저장할 수 있는 기능을 제공합니다. 이 옵션이 True로 설정되면, 편집 폼에 "새로 저장" 버튼이 추가됩니다.
        사용자가 이 버튼을 클릭하면:

        기존 객체는 변경되지 않고 유지됩니다.
        편집 폼에 입력된 데이터로 새로운 객체가 생성됩니다.
        이는 기존 객체를 템플릿으로 사용하여 유사한 객체를 빠르게 생성할 때 유용합니다.

    save_as_continue 옵션
        save_as_continue 옵션은 save_as가 활성화된 상태에서 "새로 저장" 버튼을 클릭한 후 리디렉션 동작을 제어합니다:

        True로 설정된 경우: 새로 생성된 객체의 편집 페이지로 리디렉션됩니다.
        False로 설정된 경우: 객체 목록 페이지로 리디렉션됩니다.
    """

    def date_format(value: DateTime):
        return value.strftime("%Y년 %m월 %d일 %H:%M")  # 한국식 날짜 포맷

    column_labels = {User.email: "Email"}

    # 기존 타입 포맷터 유지 + date 타입 추가
    column_type_formatters = dict(
        ModelView.column_type_formatters,  # 기본 포맷터 상속
        date=date_format,  # DateTime 타입 컬럼에 적용
    )
    save_as = True  # 기존 객체를 기반으로 새로운 객체 저장 가능

    """
    내보내기 옵션 (Export options)
    SQLAdmin은 목록(List) 페이지에서 데이터를 내보내는 기능을 지원합니다.
    현재 CSV 형식으로만 내보내기가 가능하며, 모델별로 다음과 같은 옵션을 설정할 수 있습니다.

    can_export: 해당 모델의 데이터를 내보낼 수 있는지 여부. 기본값은 True.
    column_export_list: 내보낼 데이터에 포함할 컬럼 목록. 기본값은 모든 모델 컬럼 포함.
    column_export_exclude_list: 내보낼 데이터에서 제외할 컬럼 목록.
    export_max_rows: 내보낼 최대 행(Row) 수. 기본값은 0이며, 이는 제한 없음(무제한)을 의미함.
    export_types: 활성화할 내보내기 형식 목록. 기본값은 ["csv", "json"].
    """

    """
    템플릿 (Templates)
    SQLAdmin의 템플릿 파일은 Jinja2를 기반으로 만들어졌으며, 설정을 통해 완전히 변경할 수 있습니다.
    사용 가능한 페이지 템플릿은 다음과 같습니다.

    list_template: 모델 목록 페이지에서 사용할 템플릿. 기본값은 sqladmin/list.html.
    create_template: 모델 생성 페이지에서 사용할 템플릿. 기본값은 sqladmin/create.html.
    details_template: 모델 상세 페이지에서 사용할 템플릿. 기본값은 sqladmin/details.html.
    edit_template: 모델 수정 페이지에서 사용할 템플릿. 기본값은 sqladmin/edit.html.

    list_template = "custom_list.html"

    For more information about working with template see Working with Templates.
    url : https://aminalaee.dev/sqladmin/working_with_templates/
    """

    """
    이벤트 (Events)
    모델이 생성(Create), 수정(Update) 또는 **삭제(Delete)**되기 전이나 후에 특정 동작을 수행해야 하는 경우가 있을 수 있습니다.

    이를 위해 다음 네 가지 메서드를 **오버라이드(Override)**하여 원하는 동작을 구현할 수 있습니다.

    on_model_change: 모델이 생성되거나 수정되기 전에 호출됩니다.
    after_model_change: 모델이 생성되거나 수정된 후에 호출됩니다.
    on_model_delete: 모델이 삭제되기 전에 호출됩니다.
    after_model_delete: 모델이 삭제된 후에 호출됩니다.

    async def on_model_change(self, data, model, is_created, request):
        # Perform some other action
        ...

    async def on_model_delete(self, model, request):
        # Perform some other action
        ...
    """

    """
    커스텀 액션 (Custom Action)
    Admin 패널에서 모델에 대한 **사용자 지정 액션(Custom Action)**을 추가하려면 @action 데코레이터를 사용할 수 있습니다.

    사용 가능한 액션 옵션
    name: 이 액션의 URL에서 사용할 문자열 이름.
    label: 이 액션을 설명하는 문자열.
    add_in_list: 이 액션을 목록 페이지에서 사용할 수 있도록 할지 여부를 결정하는 불리언 값.
    add_in_detail: 이 액션을 상세 페이지에서 사용할 수 있도록 할지 여부를 결정하는 불리언 값.
    confirmation_message: 이 문자열 메시지가 정의되면, 액션 메서드를 호출하기 전에 확인 메시지를 표시하는 모달 창이 나타남.

    from sqladmin import BaseView, action

    class UserAdmin(ModelView, model=User):
        @action(
            name="approve_users",
            label="Approve",
            confirmation_message="Are you sure?",
            add_in_detail=True,
            add_in_list=True,
        )
        async def approve_users(self, request: Request):
            pks = request.query_params.get("pks", "").split(",")
            if pks:
                for pk in pks:
                    model: User = await self.get_object_for_edit(pk)
                    ...

            referer = request.headers.get("Referer")
            if referer:
                return RedirectResponse(referer)
            else:
                return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    admin.add_view(UserAdmin)
    """

    # 데이터 추가때 호출되는 insert_model 메서드 오버라이드
    """
    insert_model() 메서드는 request 객체와 data 객체를 인자로 받는다.
    request 는 Starlette의 Request 객체이다.
    data 는 사전형 객체인데, 폼에 입력된 값들이다.
    여기에선 단순하게 사용자가 입력한 비밀번호가 있으면 해시해서 data 의 hashed_password 에 덮어씌운다.
    """

    async def insert_model(self, request: Request, data: dict) -> Any:
        if _password := data.get("hashed_password"):
            data["hashed_password"] = generate_password_hash(_password)
        return await super().insert_model(request, data)

    """
    데이터 변경은 update_model() 메서드를 호출한다.
    insert_model() 메서드와 다른 점은 변경 대상의 기본키값도 인자로 전달해주는 것이다.

    차이점은 변경할 때 비밀번호를 입력하면 변경 대상의 데이터를 가져와서 해시 처리되어 저장된 값과 비교하고,
    다르면 폼 데이터(payload인 data)에 새로 해시 처리한 문자열을 담는 것이다.
    동일하다는 얘기는 비밀번호를 수정하지 않아서 해시 처리된 문자열 그대로 넘어온 거니까 해시 처리하면 안 된다.
    """

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        if _password := data.get("hashed_password"):
            obj = await self.get_object_for_details(pk)
            if _password != obj.hashed_password:
                data["hashed_password"] = generate_password_hash(_password)
        return await super().update_model(request, pk, data)

    """
    계정 비밀번호 해시 처리는 더 간결하고 안전한 방법이 있다.
    바로 on_model_change() 메서드를 오버라이드하는 것이다.
    이 메서드는 모델 데이터가 변경될 때 호출되는데,
    추가(insert)와 변경(update)될 때 호출된다.

    on_model_change() 메서드 호출
    실제 추가/변경 처리
    after_model_change() 메서드 호출
    """

    async def on_model_change(
        self, data: dict, model: User, is_created: bool, request: Request
    ) -> None:
        pass
        # if _password := data.get("hashed_password"):
        #     if _password != model.hashed_password:
        #         data["hashed_password"] = generate_password_hash(_password)

    # ✅ 삭제 후 리디렉션 (예: 사용자 목록 페이지로 이동)
    # def get_delete_redirect(self):
    #     return "/admin/userprofile/"  # 삭제 후 목록으로 리디렉트

    """SQLAdmin은 Naive DateTime으로 일시 정보를 생성한다.
    다른 시간타입을 사용한다면 on_model_change()으로 수정 가능

    async def on_model_change(
        self, data: dict, model: Todo, is_created: bool, request: Request
    ) -> None:
        for key, value in data.items():
            if not isinstance(value, datetime):
                continue
            if value.utcoffset() is not None:
                continue
            data[key] = value.astimezone(UTC)"""

    """
    SQLAdmin은 두 가지 방식으로 열(Column)에 표시할 텍스트 형식을 지정할 수 있는데, 
    column_formatters 와 column_type_formatters 이 있다. 
    column_formatters 는 열(모델 필드) 단위로, 
    column_type_formatters 는 열의 값 자료형에 단위로 형식을 지정한다.

    1. 값 자료형 별로 출력 형식 잡아주기
    from typing import ClassVar
    from datetime import datetime

    ...

    column_type_formatters: ClassVar = {
        datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
    }

    2. 열(Column) 별로 출력 형식 잡아주기
    자료형(type) 대신 모델필드를 키로 사용하는 점이 다르고, 
    값에 사용할 호출가능한 객체의 인자가 두 개라는 점도 다르다.

    column_formatters: ClassVar = {
        Todo.group: lambda m, _: m.group.name,
    }

    """

    # https://puddingcamp.com/page/c83fd343-190e-4a60-b475-e14438a8978b
