# Generated by Django 3.2.6 on 2021-09-24 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_alter_event_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Status',
        ),
    ]