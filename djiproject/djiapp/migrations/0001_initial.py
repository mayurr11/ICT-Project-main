# Generated by Django 5.1 on 2024-08-11 08:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight_schedule',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('query_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('query', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('subscription_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.BooleanField(default=False)),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djiapp.flight_schedule')),
            ],
        ),
    ]
