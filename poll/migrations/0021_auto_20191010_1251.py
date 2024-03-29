# Generated by Django 2.2.4 on 2019-10-10 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0020_auto_20191010_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicetranslation',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='poll.Choice'),
        ),
        migrations.AlterField(
            model_name='polltranslation',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='poll.Poll'),
        ),
        migrations.AlterField(
            model_name='questiontranslation',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', to='poll.Question'),
        ),
        migrations.AlterField(
            model_name='requestedpoll',
            name='url_param',
            field=models.CharField(default='cb9c4c27fe654144aefe0969e87b6040', editable=False, max_length=72),
        ),
    ]
