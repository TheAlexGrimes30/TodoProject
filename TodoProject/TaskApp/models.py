from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
