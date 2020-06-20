# Generated by Django 3.0.4 on 2020-03-27 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimeStamp', models.DateTimeField(verbose_name='TimeStamp')),
                ('EventText', models.CharField(max_length=200)),
                ('TimeTaken', models.IntegerField(verbose_name='Time Taken')),
                ('RelatedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CommentText', models.CharField(max_length=250)),
                ('RelatedEvent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TimeSheet.Events')),
                ('RelatedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
