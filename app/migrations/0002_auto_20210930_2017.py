# Generated by Django 3.2.7 on 2021-09-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dummy',
            name='sub_category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dummy',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]