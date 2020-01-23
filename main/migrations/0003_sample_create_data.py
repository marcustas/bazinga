# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import random
from django.utils import timezone

from django.db import migrations, models

from main.models import Baz, User, Target


def add_data(apps, schema_editor):
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
                email='target_{}@mail.me'.format(i),
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
