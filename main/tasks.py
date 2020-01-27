from django.core import management

from bazinga.celery import app


@app.task()
def send_email_task(target_id, baz_id):
    management.call_command("send_email_to_target", target_id, baz_id)
    return "Email to target sent."


@app.task()
def schedule_tomorrow_emails():
    management.call_command("schedule_tomorrow_tasks")
    return "Tasks for tomorrow successfully scheduled."
