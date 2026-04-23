from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Field Agent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Field(models.Model):

    STAGES = [
        ('Planted', 'Planted'),
        ('Growing', 'Growing'),
        ('Ready', 'Ready'),
        ('Harvested', 'Harvested'),
    ]

    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=100)
    planting_date = models.DateField()
    current_stage = models.CharField(max_length=20, choices=STAGES)

    assigned_agent = models.ForeignKey(User, on_delete=models.CASCADE)  

    def status(self):
        from django.utils import timezone

        if self.current_stage == 'Harvested':
            return "Completed"

        days = (timezone.now().date() - self.planting_date).days

        if days > 30 and self.current_stage != 'Ready':
            return "At Risk"

        return "Active"

    def status(self):
        if self.current_stage == 'Harvested':
            return "Completed"

        from django.utils import timezone
        days = (timezone.now().date() - self.planting_date).days

        if days > 30 and self.current_stage != 'Ready':
            return "At Risk"

        return "Active"

    def status(self):
        if self.current_stage == 'Harvested':
            return "Completed"

        days = (timezone.now().date() - self.planting_date).days

        if days > 30 and self.current_stage != 'Ready':
            return "At Risk"

        return "Active"

    def __str__(self):
        return self.name




class FieldUpdate(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    agent = models.CharField(max_length=100)
    stage = models.CharField(max_length=20)
    notes = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.field.name} - {self.stage}"