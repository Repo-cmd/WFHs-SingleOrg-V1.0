# Generated by Django 3.0.4 on 2020-03-27 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeSheet', '0002_events_approvalstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='TimeTaken',
            field=models.FloatField(verbose_name='Time Taken'),
        ),
    ]
