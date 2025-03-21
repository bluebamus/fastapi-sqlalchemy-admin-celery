# celeryconfig.py

# broker_url: 메시지 브로커의 URL을 지정
broker_url = "redis://127.0.0.1:6379/0"

# result_backend: 작업 결과를 저장할 백엔드의 URL을 지정
result_backend = "db+mysql+pymysql://celery:1324@localhost/celery"

# celery beat
beat_dburi = "mysql+pymysql://celery:1324@localhost:3306/celery"

# celery beat
beat_schema = None
# task_serializer: 작업을 직렬화할 때 사용할 형식을 지정 (json, msgpack 등)
task_serializer = "json"

# result_serializer: 결과를 직렬화할 때 사용할 형식을 지정
result_serializer = "json"

# accept_content: 허용할 메시지 형식의 리스트. 여기서는 JSON 형식만 허용
accept_content = ["json"]

# enable_utc: UTC 시간대 사용을 활성화
enable_utc = True

# timezone: Celery가 사용할 기본 시간대를 설정
timezone = "UTC"

# broker_connection_retry_on_startup: 시작 시 브로커 연결 재시도를 활성화
broker_connection_retry_on_startup = True

# worker_concurrency: 동시에 실행할 worker 개수 (기본값은 CPU 코어 수)
worker_concurrency = 4  # 동시에 실행할 worker 개수

# task_acks_late: 작업이 끝난 후에만 ack 보내기 (True일 경우 작업이 성공적으로 처리된 후 ack를 보냄)
task_acks_late = True

# task_reject_on_worker_lost: 작업을 실패로 처리하고 브로커에서 삭제할지 여부 결정
# task_reject_on_worker_lost = True  # 작업이 실패로 간주되고, 워커가 분실되면 삭제됨

# result_expires: 결과가 만료되는 시간. 지정된 시간이 지나면 결과가 삭제됨
# result_expires = 3600  # 초 단위로 결과의 만료 시간을 설정 (1시간)

# task_default_queue: 기본 큐 이름 설정
task_default_queue = "default"  # 작업이 큐에 삽입될 때 사용할 기본 큐 이름

# task_default_exchange: 기본 교환기 설정
task_default_exchange = "default"  # 작업이 기본적으로 삽입될 교환기의 이름 설정

# task_default_routing_key: 기본 라우팅 키 설정
task_default_routing_key = "default"  # 작업이 기본적으로 라우팅될 라우팅 키 이름 설정

# event_queue: 이벤트 큐 설정 (실시간 모니터링을 위한 설정)
event_queue = "celeryev"  # Celery 이벤트를 전송할 큐 이름

# worker_prefetch_multiplier: 워커가 한 번에 가져올 수 있는 최대 작업 수
worker_prefetch_multiplier = 1  # 각 워커가 한 번에 가져오는 작업의 수를 제한

# task_time_limit: 작업에 할당된 최대 실행 시간. 이를 초과하면 작업이 종료됨
# task_time_limit = 300  # 최대 5분 (300초)

# task_soft_time_limit: 소프트 시간 제한. 이를 초과하면 작업이 중단되지만 종료되지 않고 처리 계속
# task_soft_time_limit = 240  # 최대 4분 (240초)

# worker_max_tasks_per_child: 한 워커가 종료될 때까지 처리할 최대 작업 수
worker_max_tasks_per_child = (
    100  # 100개의 작업을 처리한 후 워커가 종료되고 새로운 워커가 시작됨
)

# worker_shutdown_timeout: 워커가 종료되기 전에 기다리는 최대 시간
worker_shutdown_timeout = 10  # 10초 후에 워커가 종료되지 않으면 강제로 종료

# beat_scheduler: Celery Beat의 스케줄러 종류 설정
beat_scheduler = "sqlalchemy_celery_beat.schedulers:DatabaseScheduler"

# loglevel: Celery 작업 로그 레벨 설정
loglevel = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" 수준 설정

# pidfile: Celery의 PID 파일을 저장할 경로 설정
# pidfile = "/var/run/celery/celery.pid"  # Celery의 프로세스 ID를 기록할 파일 경로

# worker_log_format: 워커 로그 형식 설정
worker_log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # 로그 형식 설정
)

# worker_task_log_format: 작업별 로그 형식 설정
worker_task_log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s - Task: %(task_name)s"
)
