# Generated by Django 5.0.4 on 2024-04-24 12:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("baseapp_auth", "0003_superuserupdatelog"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="superuserupdatelog",
            name="assigner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="superuser_assigner_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
