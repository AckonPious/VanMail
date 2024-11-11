# Generated by Django 5.1.1 on 2024-11-08 11:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_created_at_alter_user_updated_at'),
        ('mail', '0010_remove_mail_recalled_remove_mail_recalled_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recall_date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recall_history', to='mail.mail')),
                ('new_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recall_new_location', to='authentication.location')),
                ('previous_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recall_previous_location', to='authentication.location')),
                ('recalled_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
