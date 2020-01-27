from smtplib import SMTPException

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from main.models import Target, Baz, SentBaz

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates restaurants with all data to test webapp.'

    def add_arguments(self, parser):
        parser.add_argument('target_id', nargs='+', type=int)
        parser.add_argument('baz_id', nargs='+', type=int)

    def handle(self, *args, **options):
        target = Target.objects.get(id=options['target_id'][0])
        baz = Baz.objects.get(id=options['baz_id'][0])
        msg = EmailMultiAlternatives(
            subject=baz.title,
            body=baz.content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[target.email]
        )
        msg.attach_alternative(baz.content, "text/html")
        try:
            msg.send()
        except SMTPException as e:
            SentBaz.objects.get_or_create(
                baz=Baz(id=target.planned_baz),
                target=target,
                timestamp=timezone.now(),
                successful=False,
                error_message="Error: {}".format(e)
            )
        else:
            SentBaz.objects.get_or_create(
                baz=baz,
                target=target,
                timestamp=timezone.now(),
                successful=True,
            )
        self.stdout.write(self.style.SUCCESS('Sent email to target {}.'.format(target.email)))
