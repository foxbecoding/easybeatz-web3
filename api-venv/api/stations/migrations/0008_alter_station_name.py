# Generated by Django 5.1.4 on 2025-03-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0007_alter_station_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(default='', max_length=90),
        ),
    ]
