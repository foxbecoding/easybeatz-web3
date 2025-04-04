# Generated by Django 5.1.4 on 2025-01-25 01:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0005_trackmp3_provided_by_eb_trackwav_provided_by_eb'),
        ('stations', '0006_alter_stationpicture_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackCollaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pubkey', models.CharField(default='', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('station', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collaborations', to='stations.station')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborators', to='albums.track')),
            ],
        ),
    ]
