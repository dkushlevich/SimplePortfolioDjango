import telegram
from asgiref.sync import async_to_sync
from django import forms
from django.conf import settings

from app.models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ("email", "name", "message")


    def send_telegram_message(self):
        name, email, message = (
            self.cleaned_data.get("name"),
            self.cleaned_data.get("email"),
            self.cleaned_data.get("message"),
        )
        message = (
            f"Recieved message from {name}:\n\n{message}\n\nEmail: {email}"
        )

        bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
        async_to_sync(bot.send_message(settings.TELEGRAM_CHAT_ID, message))
