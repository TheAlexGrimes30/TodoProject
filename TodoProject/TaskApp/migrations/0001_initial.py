# Generated by Django 5.1.4 on 2025-01-08 11:44

import TaskApp.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('deadline', models.DateTimeField(default=TaskApp.models.default_deadline)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
                'db_table': 'task',
                'ordering': ['-priority', '-deadline'],
                'indexes': [models.Index(['deadline'], name='deadline_index'), models.Index(['date_created'], name='date_created_index')],
            },
        ),
    ]
