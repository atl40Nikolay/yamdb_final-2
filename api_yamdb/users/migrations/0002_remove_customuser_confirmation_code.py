# Generated by Django 2.2.16 on 2022-07-29 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='confirmation_code',
        ),
    ]
