from celery import Celery

app = Celery(
    # 'worker',
    "celery_app",
    broker="amqp://localhost:5672",
    include=['src.tasks']
)