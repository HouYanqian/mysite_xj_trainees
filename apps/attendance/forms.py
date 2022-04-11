from django import forms

from attendance.models import AttendanceGroup


class AttendanceGroupForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = AttendanceGroup
        exclude = ['personnel', 'shift']
