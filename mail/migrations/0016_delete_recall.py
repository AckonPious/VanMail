# Generated by Django 5.1.1 on 2024-11-11 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0015_remove_recall_mail_recall_individual_mail_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Recall',
        ),
    ]
