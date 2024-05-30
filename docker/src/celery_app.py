from celery import Celery
import nltk

nltk.download('punkt')

app = Celery(
    # 'worker',
    "celery_app",
    broker="amqp://rabbitmq:5672",
    # broker="amqp://localhost:5672",
    include=['src.tasks']
)