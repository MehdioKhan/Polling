# Generated by Django 2.2.4 on 2019-09-17 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0016_auto_20190911_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollanswer',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='questionanswer',
            name='from_user',
        ),
        migrations.AlterField(
            model_name='requestedpoll',
            name='url_param',
            field=models.CharField(default='04dd4e90a0754428940b51d2bfbdf171', editable=False, max_length=72),
        ),
    ]
