# Generated by Django 3.2.7 on 2021-10-11 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20211008_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dummy',
            name='selection',
        ),
        migrations.AddField(
            model_name='dummy',
            name='answer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dummy',
            name='selection1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='dummy',
            name='selection2',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
