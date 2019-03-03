# Generated by Django 2.0.2 on 2018-10-01 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('talent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalentPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('path', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('size', models.BigIntegerField(default=0)),
                ('file_type', models.CharField(blank=True, max_length=120, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uploaded', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('caption', models.CharField(blank=True, max_length=120, null=True)),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talent_pictures', to='talent.Talent')),
            ],
            options={
                'db_table': 'talent_picture',
                'ordering': ('talent', 'updated', 'name'),
                'managed': True,
            },
        ),
    ]
