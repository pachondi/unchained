import logging
log = logging.getLogger(__name__)
from django.db import models

from app.discussions.models import GroupDiscussion

# Create your models here.

class Message(models.Model):
    is_active = models.BooleanField(default=True,null=False,blank=False)

    class Meta:
        abstract = True
        

      
class GroupDiscussionMessage(Message):
    raw_message = models.CharField(max_length=100)
    group_discussion = models.ForeignKey(GroupDiscussion, related_name="for_group")
    linked_message = models.ForeignKey('self',related_name="for_reply",null=True,blank=True)
        
    
    def get_messages_for_parent(self,gd_id):
        return [ (messages.id, messages.raw_message, messages.linked_message) for messages in self.objects.filter(group_discussion=gd_id,is_active=True) ]  
    
    def __unicode__(self):
        return str(self.id) + "- " + self.raw_message + " object"
    
    def __str__(self):
        return str(self.id) + "- " + self.raw_message +" object"
    
        class Admin:
            pass
        
        class Meta:
            pass