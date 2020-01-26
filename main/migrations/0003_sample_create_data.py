# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random

from django.utils import timezone
from django.conf import settings
from django.db import migrations, models

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from main.models import Baz, User, Target


def add_data(apps, schema_editor):
    User.objects.create_user(
        username="SuperBazinga",
        email="super_bazinga@mail.me",
        password='bazinga1234',
        is_superuser=True,
        is_staff=True
    )
    for i in range(10):
        Baz.objects.create(
            title="Baz title #{}".format(i),
            content="Baz content #{}".format(i),
        )
    users = []
    for i in range(10):
        user = User.objects.create_user(
            username='Customer #{}'.format(i),
            email='customer_{}@mail.me'.format(i),
            password='bazinga1234'
        )
        users.append(user)
    targets = []
    for customer in users:
        for i in range(100):
            email_time = timezone.now() + datetime.timedelta(seconds=random.randint(0, 86400))
            target = Target(
                customer=customer,
                weekday=random.randrange(5),
                email='Customer #{} Target_{}@mail.me'.format(customer.id, i),
                email_time=email_time
            )
            targets.append(target)
    Target.objects.bulk_create(targets)


def reverse_func(apps, schema_editor):
    Baz.objects.filter(title__icontains="Baz title").delete()
    User.objects.filter(email__icontains="customer_").delete()
    Target.objects.filter(email__icontains="target_").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_auto_20200122_1925'),
    ]

    operations = [
        migrations.RunPython(add_data, reverse_func),
    ]
