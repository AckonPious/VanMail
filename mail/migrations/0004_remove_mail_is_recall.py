# Generated by Django 5.1.1 on 2024-10-22 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_mail_is_recall'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='is_recall',
        ),
    ]
