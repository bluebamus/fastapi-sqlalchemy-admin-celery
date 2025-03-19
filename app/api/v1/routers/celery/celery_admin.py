from sqladmin import ModelView
from celery.backends.database.models import Task, TaskExtended, TaskSet
from wtforms import DateTimeField, validators
from sqlalchemy_celery_beat.models import (
    ClockedSchedule,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    PeriodicTaskChanged,
    PeriodicTask,
)


class CeleryTaskAdmin(ModelView, model=Task):
    name = "Celery Task"
    name_plural = "Celery Task List"
    category = "Celery Management"

    column_list = "__all__"

    column_sortable_list = (Task.id,)
    column_default_sort = (Task.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]


class CeleryBeatClockedScheduleAdmin(ModelView, model=ClockedSchedule):
    name = "Celery Beat ClockedSchedule"
    name_plural = "Celery Beat ClockedSchedule List"
    category = "Celery Management"

    # 또는 명시적으로 테이블 이름 지정
    model_class = ClockedSchedule
    model_class.__table__.schema = None

    column_list = (
        ClockedSchedule.id,
        ClockedSchedule.clocked_time,
    )

    form_columns = (ClockedSchedule.clocked_time,)

    form_args = {
        "clocked_time": {
            "description": "한 번만 실행해야 하는 작업이나 특정 시간에 실행되어야 하는 작업을 예약",  # 필드 레이블 설정
        }
        # 다른 필드에 대해서도 필요한 경우 설정 추가
    }

    column_sortable_list = (ClockedSchedule.id,)
    column_default_sort = (ClockedSchedule.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]


class CeleryBeatIntervalScheduleAdmin(ModelView, model=IntervalSchedule):
    name = "Celery-Beat IntervalSchedule"
    name_plural = "Celery-Beat IntervalSchedule List"
    category = "Celery Management"

    model_class = IntervalSchedule
    model_class.__table__.schema = None

    column_list = (
        IntervalSchedule.id,
        IntervalSchedule.every,
        IntervalSchedule.period,
    )

    form_columns = (
        IntervalSchedule.every,
        IntervalSchedule.period,
    )

    form_args = {
        "every": {
            "description": "Number of Periods: 작업을 다시 실행하기 전에 기다리는 간격 기간 숫자 예) 10분, 10시간",  # 필드 레이블 설정
        },
        "period": {
            "description": "Interval Period: Task runs 사이의 기간 유형 (예: 일)",  # 필드 레이블 설정
        },
    }

    column_sortable_list = (IntervalSchedule.id,)
    column_default_sort = (IntervalSchedule.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]


class CeleryBeatCrontabScheduleAdmin(ModelView, model=CrontabSchedule):
    name = "Celery-Beat CrontabSchedule"
    name_plural = "Celery-Beat CrontabSchedule List"
    category = "Celery Management"

    model_class = CrontabSchedule
    model_class.__table__.schema = None

    column_list = (
        CrontabSchedule.id,
        CrontabSchedule.minute,
        CrontabSchedule.hour,
        CrontabSchedule.day_of_week,
        CrontabSchedule.day_of_month,
        CrontabSchedule.month_of_year,
        CrontabSchedule.timezone,
    )

    form_columns = (
        CrontabSchedule.minute,
        CrontabSchedule.hour,
        CrontabSchedule.day_of_week,
        CrontabSchedule.day_of_month,
        CrontabSchedule.month_of_year,
        CrontabSchedule.timezone,
    )

    form_args = {
        "minute": {
            "description": "모두 실행하려면 '*'을 사용하세요. (예: '0,30')",  # 필드 레이블 설정
        },
        "hour": {
            "description": "모두 실행하려면 '*'을 사용하세요. (예: '8,20')",  # 필드 레이블 설정
        },
        "day_of_week": {
            "description": "모두 실행하려면 '*'을 사용하세요. 일요일은 0 또는 7, 월요일은 1입니다. (예: '0,5')",  # 필드 레이블 설정
        },
        "day_of_month": {
            "description": "모두 실행하려면 '*'을 사용하세요. (예: '1,15')",  # 필드 레이블 설정
        },
        "month_of_year": {
            "description": "모두 실행하려면 '*'을 사용하세요. (예: '1,12')",  # 필드 레이블 설정
        },
        "timezone": {
            "description": "일정을 실행할 시간대. 기본값은 UTC입니다.",  # 필드 레이블 설정
        },
    }

    column_sortable_list = (IntervalSchedule.id,)
    column_default_sort = (IntervalSchedule.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]


class CeleryBeatSolarScheduleAdmin(ModelView, model=SolarSchedule):
    name = "Celery-Beat SolarSchedule"
    name_plural = "Celery-Beat SolarSchedule List"
    category = "Celery Management"

    model_class = SolarSchedule
    model_class.__table__.schema = None

    column_list = (
        SolarSchedule.id,
        SolarSchedule.event,
        SolarSchedule.latitude,
        SolarSchedule.longitude,
    )

    form_columns = (
        SolarSchedule.event,
        SolarSchedule.latitude,
        SolarSchedule.longitude,
    )

    form_args = {
        "event": {
            "description": "일출, 일몰 등의 이벤트가 발생하는 시점",  # 필드 레이블 설정
        },
        "latitude": {
            "description": "지리적 위도, 높은 정밀도를 위해 Numeric(precision=9, scale=6) 타입을 사용합니다. 이는 위도 좌표를 소수점 이하 6자리까지 표현할 수 있어, 지리적 위치를 세밀하게 지정할 수 있습니다. 지정된 위도에서 태양 이벤트가 발생하는 시점을 계산할 때 사용됩니다.",  # 필드 레이블 설정
        },
        "longitude": {
            "description": "지리적 경도, 지정된 경도와 위도 조합으로, 태양 이벤트(예: 일출, 일몰 등)의 정확한 시각을 산출하는 데 사용됩니다.",  # 필드 레이블 설정
        },
    }

    column_sortable_list = (SolarSchedule.id,)
    column_default_sort = (SolarSchedule.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]


class CeleryBeatPeriodicTaskChangedEventAdmin(ModelView, model=PeriodicTaskChanged):
    name = "Celery-Beat PeriodicTaskChanged"
    name_plural = "Celery-Beat PeriodicTaskChanged List"
    category = "Celery Management"

    model_class = PeriodicTaskChanged
    model_class.__table__.schema = None

    column_list = (
        PeriodicTaskChanged.id,
        PeriodicTaskChanged.last_update,
    )

    column_sortable_list = (PeriodicTaskChanged.id,)
    column_default_sort = (PeriodicTaskChanged.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]


class CeleryBeatPeriodicTaskAdmin(ModelView, model=PeriodicTask):
    name = "Celery-Beat PeriodicTask"
    name_plural = "Celery-Beat PeriodicTask List"
    category = "Celery Management"

    model_class = PeriodicTask
    model_class.__table__.schema = None

    column_list = (
        PeriodicTask.id,
        PeriodicTask.name,
        PeriodicTask.task,
        PeriodicTask.args,
        PeriodicTask.kwargs,
        PeriodicTask.queue,
        PeriodicTask.exchange,
        PeriodicTask.routing_key,
        PeriodicTask.headers,
        PeriodicTask.priority,
        PeriodicTask.expires,
        PeriodicTask.expire_seconds,
        PeriodicTask.one_off,
        PeriodicTask.start_time,
        PeriodicTask.enabled,
        PeriodicTask.last_run_at,
        PeriodicTask.total_run_count,
        PeriodicTask.date_changed,
        PeriodicTask.description,
        PeriodicTask.discriminator,
        PeriodicTask.schedule_id,
    )

    form_columns = (
        PeriodicTask.name,
        PeriodicTask.task,
        PeriodicTask.args,
        PeriodicTask.kwargs,
        PeriodicTask.queue,
        PeriodicTask.exchange,
        PeriodicTask.routing_key,
        PeriodicTask.headers,
        PeriodicTask.priority,
        PeriodicTask.expires,
        PeriodicTask.expire_seconds,
        PeriodicTask.one_off,
        PeriodicTask.start_time,
        PeriodicTask.enabled,
        PeriodicTask.last_run_at,
        PeriodicTask.total_run_count,
        PeriodicTask.date_changed,
        PeriodicTask.description,
        PeriodicTask.discriminator,
        PeriodicTask.schedule_id,
    )

    form_args = {
        "name": {"description": "이 작업에 대한 짧은 설명입니다."},
        "task": {
            "description": '실행될 Celery 작업의 이름입니다. (예: "proj.tasks.import_contacts")'
        },
        "args": {
            "description": 'JSON으로 인코딩된 위치 인자들입니다. (예: ["arg1", "arg2"])'
        },
        "kwargs": {
            "description": 'JSON으로 인코딩된 키워드 인자들입니다. (예: {"argument": "value"})'
        },
        "queue": {
            "description": "CELERY_TASK_QUEUES에 정의된 큐입니다. 기본 큐를 사용하려면 None으로 설정합니다."
        },
        "exchange": {
            "description": "저수준 AMQP 라우팅을 위한 Exchange를 재정의합니다."
        },
        "routing_key": {
            "description": "저수준 AMQP 라우팅을 위한 라우팅 키를 재정의합니다."
        },
        "headers": {
            "description": "AMQP 메시지를 위한 JSON으로 인코딩된 메시지 헤더입니다."
        },
        "priority": {
            "description": "0부터 255까지의 우선순위 번호입니다. (RabbitMQ, Redis에서 지원되며, 0이 가장 높은 우선순위입니다.)"
        },
        "expires": {
            "description": "해당 날짜 및 시간 이후에는 스케줄이 작업을 실행하지 않습니다."
        },
        "expire_seconds": {
            "description": "초 단위의 시간 차이로, 이 시간이 지나면 스케줄이 작업을 실행하지 않습니다."
        },
        "one_off": {
            "description": "True인 경우, 스케줄은 작업을 단 한 번만 실행합니다."
        },
        "start_time": {
            "description": "스케줄이 작업 실행을 시작할 시작 날짜 및 시간입니다."
        },
        "enabled": {
            "description": "스케줄을 활성화하려면 True, 비활성화하려면 False로 설정합니다."
        },
        "last_run_at": {
            "description": "스케줄이 마지막으로 작업을 실행한 날짜 및 시간입니다."
        },
        "total_run_count": {"description": "스케줄이 작업을 실행한 총 횟수입니다."},
        "date_changed": {
            "description": "이 PeriodicTask가 마지막으로 수정된 날짜 및 시간입니다."
        },
        "description": {"description": "이 Periodic Task의 상세한 설명입니다."},
        "discriminator": {"description": "스케줄 클래스의 소문자 이름입니다."},
        "schedule_id": {"description": "스케줄 모델 객체의 ID입니다."},
    }

    column_sortable_list = (PeriodicTask.id,)
    column_default_sort = (PeriodicTask.id, True)

    page_size = 25
    page_size_options = [25, 50, 100, 200]
