from django import forms
from .models import Tweet
from django.conf import settings

MAX_LENGTH = settings.MAX_LENGTH


class TweetForm(forms.ModelForm):
    # declare form
    class Meta:
        model = Tweet
        fields = ['content']

    # validate and clean content going to our database
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("Tweet is too long")
        return content
