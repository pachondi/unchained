from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import default
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_protect
from south.modelsinspector import timezone
from token import EQUAL
from test.test_imageop import MAX_LEN
from app.geography.models import Country, State


ACCESS_LEVEL = ((1,'Public'), (2,'Network'), (3,'Connections'), (4,'You'))

class SiteUser(User):
    user_slug = models.CharField(max_length=128)
    dob=models.DateField(default=timezone.now())
    is_verified = models.BooleanField(default=False)    
    sent_requests = models.ManyToManyField('self',symmetrical=False, related_name='requests')
    my_requests = models.ManyToManyField('self',symmetrical=False, related_name='pending')
    connections = models.ManyToManyField('self')
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
    
    def validate(self):        
        if self.first_name == "":
            raise ValidationError("First name cannot be empty")
        if self.email == "":
            return False
        if self.username == "":
            return False
    
    def create_settings(self):
        user_settings = UserSettings()
        user_settings.user = self
        user_settings.save()
    
    #def add_to_network(self):
    #    node_user = NodeUser()
    #    node_user.user_id = self.id
    #    node_user.name = self.first_name + ' ' + self.last_name        
    #    node_user.save()
        
class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(SiteUser,related_name='from_user')
    to_user = models.ForeignKey(SiteUser, related_name='to_user')
    status = models.CharField(max_length=1)
    request_dt = models.DateTimeField(default=datetime.now())
    accept_dt = models.DateTimeField(default=datetime.now())   

        
class UserPost(models.Model):
    user = models.ForeignKey(SiteUser)
    message = models.CharField(max_length=2048)
    post_by = models.ForeignKey(SiteUser, related_name='post_by')
    post_dt = models.DateTimeField(default=datetime.now())
        
class PostComment(models.Model):    
    post = models.ForeignKey(UserPost)    
    message = models.CharField(max_length=2048)
    comment_by = models.ForeignKey(SiteUser)
    commented_dt = models.DateTimeField(default=datetime.now())
    
class UserProfile(models.Model):
    user = models.ForeignKey(SiteUser)
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)
    mobile=models.CharField(max_length=16)
    #photo=models.ImageField(upload_to=settings.IMAGE_UPLOAD_PATH, blank=True)
    #thumbnail = models.ImageField(upload_to=settings.THUMBNAIL_UPLOAD_PATH)
    #postal_code = models.CharField(max_length=16)
    CURRENTLY_CHOICES = (('S','Student'),('E','Employed'),('J','JobSeeker'))
    currently = models.CharField(max_length=1, choices=CURRENTLY_CHOICES,default='S')
    
#is_activity_broadcast : 0-Your activity will not be published, 1-your activity will be published.
#broadcast_level: Restricts who can view your activity.
#network_trace_level: Who can look into your network.
class UserSettings(models.Model):
    user = models.OneToOneField(SiteUser, primary_key=True)
    is_activity_broadcast = models.BooleanField(default=True)
    broadcast_level = models.IntegerField(choices=ACCESS_LEVEL, default=3)
    network_trace_level = models.IntegerField(choices=ACCESS_LEVEL, default=3)
    
    def get_notification_settings(self):
        try:
            user_notifications = UserNotification.objects.filter(user=self.user)
        except UserNotification.DoesNotExist:
            user_notifications = UserNotification()
            
        user_notification_ids = set(user_notification.id for user_notification in user_notifications)
        selected_notifications=NotificationType.objects.all()
        for notification in selected_notifications:
            if notification.id in user_notification_ids:
                notification.is_default_enabled = not notification.is_default_enabled
            

        return selected_notifications
    
    def set_notification_settings(self, selected_notifications):
        
        for selected_notification in selected_notifications:
            notification = NotificationType.objects.get(pk=selected_notification.id)
            user_notify = UserNotification.objects.filter(user=self.user).filter(notificationtype=notification)
            if user_notify.exists():
                if notification.is_default_enabled is selected_notification.is_default_enabled:               
                    user_notify.delete()
            else:
                if notification.is_default_enabled != selected_notification.is_default_enabled:
                    user_notify = UserNotification()
                    user_notify.user=self.user
                    user_notify.notificationtype=notification
                    user_notify.save()
                
    
class NotificationType(models.Model):
    type = models.CharField(max_length=256)
    is_default_enabled = models.BooleanField(default=True)
    
class UserNotification(models.Model):
    user = models.ForeignKey(SiteUser)
    notificationtype = models.ForeignKey(NotificationType)
    
    
    