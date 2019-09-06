# Generated by Django 2.2.4 on 2019-09-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0013_auto_20190904_1432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ('-created', '-value')},
        ),
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='pollanswer',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='questionanswer',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='requestedpoll',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='requestedpoll',
            name='url_param',
            field=models.CharField(default='98062f115c9e4f9bb82fcbf55c26683f', editable=False, max_length=72),
        ),
    ]
