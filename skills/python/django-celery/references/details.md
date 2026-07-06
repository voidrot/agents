# Django Celery — Detailed Reference

## Installation

```bash
pip install celery[redis] django-celery-results django-celery-beat
```

## Celery App Entrypoint

```python
# config/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

```python
# config/__init__.py
from .celery import app as celery_app

__all__ = ("celery_app",)
```

## Django Settings

```python
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="django-db")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
```

## Running Workers

```bash
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A config worker --loglevel=warning --concurrency=4 -Q default,high_priority
```

Do not run worker and Beat combined in production; it risks duplicate schedules and weak process isolation.

## Task Design

```python
# apps/notifications/tasks.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(name="notifications.send_welcome_email")
def send_welcome_email(user_id: int) -> None:
    from apps.users.models import User
    from apps.notifications.services import EmailService

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("send_welcome_email: user %s not found", user_id)
        return

    EmailService.send_welcome(user)
```

## Retryable Task

```python
@shared_task(
    bind=True,
    name="integrations.sync_to_crm",
    max_retries=5,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def sync_contact_to_crm(self, contact_id: int) -> dict:
    from apps.crm.services import CRMClient

    try:
        return CRMClient().sync(contact_id)
    except CRMClient.RateLimitError as exc:
        raise self.retry(exc=exc, countdown=int(exc.retry_after))
```

## Idempotent ORM Updates

```python
@shared_task(name="orders.mark_shipped")
def mark_order_shipped(order_id: int, tracking_number: str) -> None:
    from apps.orders.models import Order

    Order.objects.filter(
        pk=order_id,
        status=Order.Status.PROCESSING,
    ).update(
        status=Order.Status.SHIPPED,
        tracking_number=tracking_number,
    )
```

## Beat Schedules

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "cleanup-expired-sessions": {
        "task": "users.cleanup_expired_sessions",
        "schedule": crontab(hour=2, minute=0),
    },
}
```

For database-managed schedules, use `django_celery_beat.models.PeriodicTask` and keep only one Beat scheduler active.

## Canvas Workflows

```python
from celery import chain, group, chord

pipeline = chain(fetch_data.s(source_id), transform_data.s(), load_to_warehouse.s())
parallel = group(send_welcome_email.s(user_id) for user_id in new_user_ids)
result = chord(group(process_chunk.s(chunk) for chunk in chunks), aggregate_results.s())
```

## Failure Capture and Dead-Letter Records

```python
from celery.signals import task_failure

@task_failure.connect
def on_task_failure(sender, task_id, exception, args, kwargs, traceback, einfo, **kw):
    logger.exception(
        "Celery task failed",
        extra={"task": sender.name, "task_id": task_id, "args": args, "kwargs": kwargs},
    )
```

For permanently failed business operations, persist a model/table row with task ID, input IDs, error, and retry count for manual review.

## Testing Celery Tasks

```python
# config/settings/test.py
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
```

```python
@pytest.mark.django_db
def test_registration_triggers_welcome_email(client):
    with patch("apps.notifications.services.EmailService") as mock_email:
        response = client.post("/api/users/", {"email": "new@example.com"})

    assert response.status_code == 201
    mock_email.send_welcome.assert_called_once()
```

Unit-test task bodies directly when possible. Use eager mode for integration paths, but remember it does not perfectly model broker/worker retry behavior.

## Monitoring Checklist

- Inspect workers: `celery -A config inspect active`, `stats`, `reserved`.
- Track queue length in Redis/RabbitMQ.
- Use Flower or platform-native monitoring for visibility.
- Alert on queue depth, worker crash loops, retry spikes, and Beat duplication.
- Ensure worker process management restarts failed workers.

## Anti-Patterns

- Passing ORM model instances instead of IDs.
- Blocking request handlers waiting for Celery results.
- Retrying non-idempotent payment or fulfillment tasks without guards.
- Running Beat on multiple nodes unintentionally.
- Using late acknowledgments on tasks that cannot safely rerun.
