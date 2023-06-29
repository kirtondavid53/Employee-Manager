from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, default="")
    email_address = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    details = models.TextField(default="")
    salary = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
