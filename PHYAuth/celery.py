import os
from abc import ABC

from celery import Celery, Task, shared_task
from django.core.mail import EmailMessage
from django.db import transaction

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PHYAuth.settings')

app = Celery('PHYAuth')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


class TransactionAwareTask(Task, ABC):
    """
    Task class which is aware of django db transactions and only executes tasks
    after transaction has been committed
    """
    abstract = True

    def apply_async(self, *args, **kwargs):
        """
        Unlike the default task in celery, this task does not return an async result
        """
        transaction.on_commit(
            lambda: super(TransactionAwareTask, self).apply_async(
                *args, **kwargs))


@shared_task(base=TransactionAwareTask, bind=True, rate_limit='6/m')
def my_send_mail(self, subject, html_content, from_email, to):
    msg = EmailMessage(subject=subject, body=html_content, from_email=from_email, to=to)
    msg.content_subtype = "html"
    try:
        msg.send()
    except Exception as e:
        """
        邮件发送失败，使用retry进行重试
        retry的参数可以有：
            exc：指定抛出的异常
            throw：重试时是否通知worker是重试任务
            eta：指定重试的时间／日期
            countdown：在多久之后重试（每多少秒重试一次）
            max_retries：最大重试次数
        """
        raise self.retry(exc=e, countdown=60 * 5, max_retries=5)
