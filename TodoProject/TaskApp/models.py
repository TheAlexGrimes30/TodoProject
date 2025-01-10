from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from AuthApp.models import CustomUser
from unidecode import unidecode


def default_deadline():
    return timezone.now() + timedelta(days=1)

class Task(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    deadline = models.DateTimeField(default=default_deadline)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks", default=1)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(unidecode(self.title))
            count = 1
            while Task.objects.filter(slug=slug).exists():
                slug = f"{slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        db_table = "task"
        verbose_name = "task"
        verbose_name_plural = "tasks"
        ordering = ['-priority', '-deadline']
        indexes = [
            models.Index(['deadline'], name='deadline_index'),
            models.Index(['date_created'], name='date_created_index'),
        ]
