# Generated by Django 5.1.4 on 2025-03-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0009_alter_station_email_alter_station_handle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='handle',
            field=models.CharField(default='', max_length=90, unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(default='', max_length=90),
        ),
    ]
