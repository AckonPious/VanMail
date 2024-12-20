# Generated by Django 5.1.1 on 2024-11-11 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_created_at_alter_user_updated_at'),
        ('mail', '0016_delete_recall'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_id', models.CharField(max_length=100)),
                ('recalled_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('current_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_recalls', to='authentication.location')),
                ('new_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_recalls', to='authentication.location')),
                ('recalled_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
