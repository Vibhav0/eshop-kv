from django.views.generic.base import TemplateView
from django.conf import settings
class HomePageView(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["key"]=settings.STRIPE_PUBLISHABLE_KEY
        return context

