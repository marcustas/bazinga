import datetime
from io import StringIO

from django.core.management import call_command
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from test_plus import TestCase

from main.models import Target, Baz, SentBaz

User = get_user_model()


class BazingaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.first()
        self.password = 'bazinga1234'
        self.tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).weekday()

    def test_thank_you_page(self):
        response = self.get('thank-you')
        self.response_200(response)

    def test_set_interval_page_get(self):
        self.assertLoginRequired('set-interval')

        with self.login(username=self.user.username, password=self.password):
            response = self.get('set-interval')
            self.response_200(response)

    def test_set_interval_page_post(self):
        new_interval = self.user.interval + 2
        with self.login(username=self.user.username, password=self.password):
            response = self.post('set-interval', data={'interval': new_interval})
            user = User.objects.get(id=self.user.id)
            self.assertRedirects(
                response,
                reverse('thank-you'),
                status_code=302,
                target_status_code=200
            )
            self.assertEqual(user.interval, new_interval)

    def test_schedule_command(self):
        out = StringIO()
        call_command('schedule_tomorrow_tasks', stdout=out)
        self.assertIn('Created tasks for', out.getvalue())

    def send_email_task(self, exception=False):
        out = StringIO()
        call_command('schedule_tomorrow_tasks')
        target = Target.objects.only('id').order_by("?").first()
        baz = Baz.objects.only('id').order_by("?").first()
        call_command('send_email_to_target', target.id, baz.id, stdout=out)
        self.assertIn('Sent email to target', out.getvalue())
        try:
            sent_baz = SentBaz.objects.get(target=target, baz=baz)
        except SentBaz.DoesNotExist:
            self.fail(self._formatMessage('SentBaz instance was not created after task execution.', ''))
        except SentBaz.MultipleObjectsReturned:
            self.fail(self._formatMessage('SentBaz has duplicates with same target and baz.', ''))
        if exception:
            self.assertFalse(sent_baz.successful)
            self.assertIsNotNone(sent_baz.error_message)
        else:
            self.assertTrue(sent_baz.successful)
            self.assertIsNone(sent_baz.error_message)

    def test_send_email_task(self):
        self.send_email_task()

    def test_send_email_wrong_email_settings(self):
        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
                EMAIL_HOST='smtp.gmail.com',
                EMAIL_HOST_USER='wrong_user@gmail.com',
                EMAIL_HOST_PASSWORD='wrong_password'
        ):
            self.send_email_task(exception=True)
