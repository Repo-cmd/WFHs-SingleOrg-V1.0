# Generated by Django 3.0.4 on 2020-04-05 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheet', '0005_extrapermissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extrapermissions',
            options={'permissions': [('EventsMiddleLayerAdmin', 'Group(s) Admin'), ('EventsSuperAdmin', 'Super Admin')]},
        ),
    ]