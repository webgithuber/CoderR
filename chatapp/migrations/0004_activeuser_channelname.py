# Generated by Django 4.1.3 on 2022-12-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_activeuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeuser',
            name='channelname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
