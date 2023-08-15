from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


    class Meta:
        fields = ("email", "name", "message")
