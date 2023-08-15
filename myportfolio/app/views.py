from django.contrib.auth import get_user_model
from django.views.generic import FormView

from app.forms import ContactForm
from app.models import Instrument, Project

User = get_user_model()

class PortfolioView(FormView):
    template_name = "base.html"
    form_class = ContactForm
    success_url = "/#contact"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = User.objects.first()
        context["user"] = user
        context["projects"] = Project.objects.filter(author=user).all()
        context["frontend_instruments"] = (
            Instrument.objects.filter(
                owner=user, development_type=Instrument.FRONTEND,
            ).all()
        )
        context["backend_instruments"] = Instrument.objects.filter(
            owner=user, development_type=Instrument.BACKEND,
        ).all()
        return context

    def form_valid(self, form):
        #form.send_email()
        return super().form_valid(form)
