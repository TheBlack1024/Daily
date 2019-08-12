#coding=utf-8

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Daily

class DailyForm(forms.ModelForm):

    class Meta:
        model = Daily
        fields = (
            'title','tag','category','content',
        )

    class media:
        js = ('animations.js','actions.js')