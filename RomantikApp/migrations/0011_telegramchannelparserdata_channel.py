# Generated by Django 4.2 on 2024-03-16 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RomantikApp', '0010_telegramchannelparserdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramchannelparserdata',
            name='channel',
            field=models.CharField(default='tk_romantik', max_length=45),
            preserve_default=False,
        ),
    ]
