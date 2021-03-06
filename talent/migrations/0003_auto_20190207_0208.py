# Generated by Django 2.0.5 on 2019-02-07 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0002_talent_tid'),
    ]

    operations = [
        migrations.AddField(
            model_name='talent',
            name='abbreviated_key',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AddField(
            model_name='talent',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
