import datetime

from django.db.models import F, Subquery, OuterRef, Count, ExpressionWrapper, IntegerField
from django.db.models.functions import Coalesce
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

from celery.utils.log import get_task_logger
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from bazinga.celery import app
from main.models import Target, Baz, User, SentBaz


logger = get_task_logger(__name__)


@app.task
def send_email_task(target_id, baz_id):
    target = Target.objects.get(id=target_id)
    baz = Baz.objects.get(id=baz_id)
    msg = EmailMultiAlternatives(
        subject=baz.title,
        body=baz.content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[target.email]
    )
    msg.attach_alternative(baz.content, "text/html")
    msg.send()
    SentBaz.objects.create(
        baz=Baz(id=target.planned_baz),
        target=target,
        timestamp=timezone.now()
    )


@app.task
def schedule_tomorrow_emails():
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='*',
        hour='23',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )
    PeriodicTask.objects.create(
        crontab=schedule,
        name='Prepare tasks for tomorrow',
        task='main.tasks.schedule_tomorrow_emails',
    )
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).weekday()
    planned_bazes_qs = Baz.objects.exclude(
        sent_to_targets__target=OuterRef("id")
    ).only('sent_to_targets__target')
    customers = User.objects.prefetch_related('user_targets') \
                            .filter(user_targets__isnull=False)\
                            .annotate(
                                targets_count=Count('user_targets'),
                                targets_once=ExpressionWrapper(
                                    F('targets_count') / F('interval') + 1, output_field=IntegerField()),
                            )
    periodic_tasks = []
    for customer in customers:
        all_targets = customer.user_targets.annotate(
            planned_baz=Subquery(planned_bazes_qs.values('id')[:1]),
            count_sent=Coalesce(Subquery(
                Baz.objects.filter(sent_to_targets__target=OuterRef("id"))
                           .only('sent_to_targets__target')
                           .values('sent_to_targets__target')
                           .annotate(count=Count('pk'))
                           .values('count')
            ), 0)
        ).order_by('count_sent')
        tomorrow_targets = [target for target in all_targets if target.weekday == str(tomorrow)]
        for target in tomorrow_targets:
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=target.email_time.minute,
                hour=target.email_time.hour,
                day_of_week=target.weekday,
                day_of_month='*',
                month_of_year='*',
            )
            PeriodicTask.objects.create(
                crontab=schedule,
                name='Send Bazinga to {}'.format(target.email),
                task='main.tasks.send_email_task',
                args=[target.id, target.planned_baz],
                one_off=True
            )
