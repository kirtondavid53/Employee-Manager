from django.forms import ModelForm
from .models import Employee

class AddEmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ("user",)