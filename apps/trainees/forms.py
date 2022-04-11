from django import forms
from .models import TraineesInterview, Trainees


class TraineesInterviewForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = TraineesInterview
        # exclude = ('tally_type',)


class TraineesForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Trainees