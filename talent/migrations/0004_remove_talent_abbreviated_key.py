# Generated by Django 2.0.5 on 2019-02-07 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0003_auto_20190207_0208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talent',
            name='abbreviated_key',
        ),
    ]
