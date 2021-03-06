# Generated by Django 3.2.7 on 2021-10-05 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0002_auto_20211004_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApproverNotification',
            fields=[
                ('notifcation_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('linkCreated', models.BooleanField(default=False)),
                ('excelLink', models.URLField(blank=True, null=True)),
                ('emailSend', models.BooleanField(default=False)),
                ('workDone', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approver_notification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AproverNotification',
        ),
    ]
