from django.contrib import messages
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

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.INFO,
            "Message Sent! Thank you for contacting me.",
        )
        return super().get_success_url()

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            "Something went wrong! Please try again.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        form.send_telegram_message()
        return super().form_valid(form)
