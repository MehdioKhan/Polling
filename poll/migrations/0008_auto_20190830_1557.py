# Generated by Django 2.2.4 on 2019-08-30 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0007_auto_20190830_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedpoll',
            name='url',
            field=models.CharField(default='e5f7aa37f9bb457c9c91fae25c0beb4e', editable=False, max_length=72),
        ),
    ]
