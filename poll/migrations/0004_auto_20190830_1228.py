# Generated by Django 2.2.4 on 2019-08-30 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0003_pollanswer_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollanswer',
            name='user',
        ),
        migrations.AddField(
            model_name='pollanswer',
            name='from_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answered_to', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pollanswer',
            name='to_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
