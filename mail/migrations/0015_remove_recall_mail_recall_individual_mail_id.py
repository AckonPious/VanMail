# Generated by Django 5.1.1 on 2024-11-10 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0014_mail_recalled_recall'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recall',
            name='mail',
        ),
        migrations.AddField(
            model_name='recall',
            name='individual_mail_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
