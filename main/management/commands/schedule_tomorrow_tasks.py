import datetime
import itertools

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import F, Subquery, OuterRef, Count, ExpressionWrapper, IntegerField
from django.db.models.functions import Coalesce
from django.conf import settings

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from main.models import Baz

User = get_user_model()


class Command(BaseCommand):
    help = 'Schedules email tasks for tomorrow.'

    def handle(self, *args, **options):
        PeriodicTask.objects.filter(enabled=False, one_off=True).delete()
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).weekday()
        planned_bazes_qs = Baz.objects.exclude(
            sent_to_targets__target=OuterRef("id")
        ).only('sent_to_targets__target')
        customers = User.objects.prefetch_related('user_targets') \
            .filter(user_targets__isnull=False) \
            .annotate(
            targets_count=Count('user_targets'),
            targets_once=ExpressionWrapper(
                F('targets_count') / F('interval') + 1, output_field=IntegerField()),
        ).exclude(targets_once=0)
        periodic_tasks = []
        count_tasks = 0
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
            all_targets = (target for target in all_targets if target.weekday == str(tomorrow))
            tomorrow_targets = itertools.islice(all_targets, customer.targets_once)
            for target in tomorrow_targets:
                schedule, _ = CrontabSchedule.objects.get_or_create(
                    minute=target.email_time.minute,
                    hour=target.email_time.hour,
                    day_of_week=target.weekday,
                    day_of_month='*',
                    month_of_year='*',
                    timezone=settings.CELERY_TIMEZONE
                )
                new_task = PeriodicTask(
                    crontab=schedule,
                    name='Send Bazinga to {}'.format(target.email),
                    task='main.tasks.send_email_task',
                    args=[target.id, target.planned_baz],
                    one_off=True,
                )
                periodic_tasks.append(new_task)
                count_tasks += 1
        PeriodicTask.objects.bulk_create(periodic_tasks, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS('Created tasks for {} users.'.format(count_tasks)))
