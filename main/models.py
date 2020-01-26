import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from tinymce.models import HTMLField


class User(AbstractUser):
    """
    Model to hold information about Customer.
    """
    interval = models.PositiveSmallIntegerField(_("Scheduling interval"), default=1)


class Target(models.Model):
    """
    Customers target for emails
    """
    MONDAY = '0'
    TUESDAY = '1'
    WEDNESDAY = '2'
    THURSDAY = '3'
    FRIDAY = '4'
    WEEKDAYS = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
    ]
    weekday = models.CharField(_("Weekday"), choices=WEEKDAYS, default=MONDAY, max_length=20)
    email_time = models.TimeField(_("Email time"), default=datetime.time(12, 0))
    email = models.EmailField(_("Email"))
    customer = models.ForeignKey(
        'main.User', verbose_name=_("Customer"), on_delete=models.CASCADE, related_name='user_targets'
    )

    def __str__(self):
        return self.email


class Baz(models.Model):
    """
    New cool products Bazinga
    """
    title = models.CharField(_("Title"), max_length=255)
    content = HTMLField(verbose_name=_("Content"))

    def __str__(self):
        return self.title


class SentBaz(models.Model):
    """
    Model to hold relations between sent  bazes and targets
    """
    baz = models.ForeignKey(
        'main.Baz', verbose_name=_("Baz"), on_delete=models.CASCADE, related_name='sent_to_targets'
    )
    target = models.ForeignKey(
        'main.Target', verbose_name=_("Target"), on_delete=models.CASCADE, related_name='sent_bazes'
    )
    timestamp = models.DateTimeField(_('Sent datetime'))
    successful = models.BooleanField(_('Is email sending was successful'), default=False)
    error_message = models.TextField(_('Error message'), null=True, blank=True)

    def __str__(self):
        return "Sent {} to {}".format(self.baz, self.target)
