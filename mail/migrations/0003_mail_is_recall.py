# Generated by Django 5.1.1 on 2024-10-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_mail_is_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='is_recall',
            field=models.BooleanField(default=False),
        ),
    ]