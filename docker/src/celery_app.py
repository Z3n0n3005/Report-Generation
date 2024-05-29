from celery import Celery

app = Celery(
    # 'worker',
    "celery_app",
    # broker="amqp://rabbitmq:5672",
    broker="amqp://localhost:5672",
    # backend=tasks.get_result_backend()
    # backend="amqp://rabbitmq:5672",
    include=['src.tasks']
)