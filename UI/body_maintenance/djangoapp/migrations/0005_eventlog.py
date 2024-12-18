# Generated by Django 4.2.7 on 2024-12-12 06:49

from django.db import migrations, models
import djangoapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0004_access_module_apiresource_config_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('Interlocking', 'Interlocking'), ('Batch logs', 'Batch logs'), ('User logs', 'User Logs'), ('Configurations', 'Configurations')], max_length=50, verbose_name='Event Type')),
                ('event', models.CharField(choices=[('Insert', 'Insert'), ('Update', 'Update'), ('Delete', 'Delete'), ('Lock', 'Lock'), ('Unlock', 'Unlock'), ('Login', 'Login'), ('Logout', 'Logout'), ('Failed', 'Failed')], max_length=10, verbose_name='Events')),
                ('event_description', models.TextField(verbose_name='Event Description')),
                ('user', models.CharField(blank=True, max_length=200, null=True, verbose_name='User')),
                ('device_unique_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Device')),
                ('batch_unique_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Inventory')),
                ('timestamp', models.DateTimeField(default=djangoapp.models.get_current_dt, verbose_name='Timestamp')),
                ('metadata', models.JSONField(blank=True, null=True, verbose_name='Metadata')),
            ],
            options={
                'verbose_name': 'Event Log',
                'verbose_name_plural': 'Event Logs',
                'db_table': 'djangoapp_event_logs',
                'ordering': ['-timestamp'],
            },
        ),
    ]
