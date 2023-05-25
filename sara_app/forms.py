from django import forms
from .models import Event,Employees

class save_event(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','date']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['empid','name', 'email', 'phone', 'profilepic']