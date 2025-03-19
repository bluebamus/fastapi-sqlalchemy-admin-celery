# fastapi-sqlalchemy-admin-celery
Install sqlalchemy admin using alembic for fastapi-based projects and connect celery and celery-beat.

# celery
The moment a request for a Celery task is initiated, a table is created in the database to store the results.

## how to start
1. celery command for window
- celery -A main.celery_app worker -l info -P gevent

2. celery beat command
- celery -A main.celery_app beat -S sqlalchemy_celery_beat.schedulers:DatabaseScheduler -l info