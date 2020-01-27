from django.core import management

from celery.utils.log import get_task_logger

from bazinga.celery import app

logger = get_task_logger(__name__)


@app.task()
def send_email_task(target_id, baz_id):
    management.call_command("send_email_to_target", target_id, baz_id)
    logger.info("Email to target sent.")


@app.task()
def schedule_tomorrow_emails():
    management.call_command("schedule_tomorrow_tasks")
    logger.info("Tasks for tomorrow successfully scheduled..")
