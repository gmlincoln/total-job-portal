# Generated by Django 5.0.7 on 2024-10-28 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruitermodel',
            name='company_info',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
