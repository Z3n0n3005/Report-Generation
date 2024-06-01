from celery import Celery
import nltk

nltk.download('punkt')

app = Celery(
    "app",
    broker="redis://redis:6379",
    # broker="redis://localhost:5672",
    backend="redis://redis:6379", 
    include=["src.tasks"]
)
# import tasks
# app.autodiscover_tasks(force=True)
# # Create an inspector instance
# i = app.control.inspect()

# # Get registered tasks
# registered_tasks = i.registered()

# print("Registered Tasks:")
# for worker, tasks in registered_tasks.items():
#     print(f"Worker: {worker}")
#     for task in tasks:
#         print(f"  - {task}")