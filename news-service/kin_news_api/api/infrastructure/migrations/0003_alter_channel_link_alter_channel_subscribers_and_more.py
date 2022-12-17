# Generated by Django 4.1.2 on 2022-10-22 19:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_remove_channel_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='link',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='link'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ChannelRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.channel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'channel')},
            },
        ),
    ]
