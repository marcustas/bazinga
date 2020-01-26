from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin

User = get_user_model()


class SetIntervalView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('interval',)
    template_name = 'set_interval.html'
    success_url = reverse_lazy('thank-you')

    def get_object(self, queryset=None):
        return self.request.user


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'


class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # import datetime
        # from django.db.models import F, Subquery, OuterRef, Count, ExpressionWrapper, IntegerField, Value
        # from django.db.models.functions import Cast, Coalesce
        # from main.models import Target, Baz, User, SentBaz
        #
        # tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).weekday()
        # planned_bazes_qs = Baz.objects.exclude(
        #     sent_to_targets__target=OuterRef("id")
        # ).only('sent_to_targets__target')
        # customers = User.objects.prefetch_related('user_targets') \
        #     .filter(user_targets__isnull=False) \
        #     .annotate(
        #     targets_count=Count('user_targets'),
        #     targets_once=ExpressionWrapper(
        #         F('targets_count') / F('interval') + 1, output_field=IntegerField()),
        # )
        # for customer in customers:
        #     all_targets = customer.user_targets.annotate(
        #         planned_baz=Subquery(planned_bazes_qs.values('id')[:1]),
        #         count_sent_w_none=Coalesce(Subquery(
        #             Baz.objects.filter(sent_to_targets__target=OuterRef("id"))
        #                        .only('sent_to_targets__target')
        #                        .values('sent_to_targets__target')
        #                        .annotate(count=Count('pk'))
        #                        .values('count'),
        #         ), 0),
        #     ) \
        #         .order_by('count_sent')
        #     tomorrow_targets = [target for target in all_targets if target.weekday == str(tomorrow)]
        #     for target in tomorrow_targets:
        #         print('target', target.planned_baz, target.count_sent_w_none, target.count_sent)
        #         print('send email')
        ctx['test'] = 'test2'
        print('checkcheckcheckcheckcheckcheckcheckcheckcheck')
        return ctx