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
