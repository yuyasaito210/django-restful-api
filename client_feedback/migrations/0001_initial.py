# Generated by Django 2.0.5 on 2019-01-11 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_client_feedbacks', to='client.Client')),
            ],
            options={
                'db_table': 'client_feedback',
                'ordering': ('id', 'client', 'created'),
                'managed': True,
            },
        ),
    ]
