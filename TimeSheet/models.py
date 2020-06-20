from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Events(models.Model):
    RelatedUser = models.ForeignKey(User,on_delete=models.CASCADE)
    TimeStamp = models.DateTimeField("TimeStamp")
    EventText = models.CharField(max_length=200)
    TimeTaken = models.FloatField('Time Taken')
    ApprovalStatus = models.CharField(max_length=5,choices=[('APP','APPROVED'),('RE','REJECTED'),('SUB','SUBMITTED')], default='SUB')
    def __str__(self):
        return self.EventText

class Comments(models.Model):
    RelatedEvent = models.ForeignKey(Events, on_delete=models.CASCADE)
    RelatedUser = models.ForeignKey(User , on_delete= models.CASCADE)
    CommentText = models.CharField(max_length=250)
    TimeStamp = models.DateTimeField("TimeStamp")
    def __str__(self):
        return self.CommentText

class ExtraPermissions(models.Model):
    class Meta:
        permissions = [
            ('EventsMiddleLayerAdmin', 'Group(s) Admin'),
            ('EventsSuperAdmin', 'Super Admin')
        ]