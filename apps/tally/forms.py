from django import forms
from .models import Computer, Personnel, CheckRecord, Monitor


class ComputerForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Computer
        # exclude = ('tally_type',)


class MonitorForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Monitor


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = '__all__'
        # error_messages = {
        # }


class CheckRecordForm(forms.ModelForm):
    class Meta:
        model = CheckRecord
        exclude = ('monitor',)