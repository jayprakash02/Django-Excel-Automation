# Generated by Django 3.2.7 on 2021-10-03 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210930_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feelings', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='lifevector',
            name='sitution',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='feelings',
            name='emotion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feelings_emotion', to='app.emotion'),
        ),
    ]