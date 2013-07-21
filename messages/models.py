from django.db import models

from discussions.models import GroupDiscussion

# Create your models here.

class Message(models.Model):
    pass

    class Meta:
        abstract = True
        
        
class GroupDiscussionMessage(Message):
    raw_message = models.CharField(max_length=100)
    group_discussion = models.ForeignKey(GroupDiscussion)
    
    def get_messages_for_parent(self,gd_id):
        return [ (messages.id, messages.raw_message) for messages in self.objects.filter(group_discussion=gd_id) ]  
    
    def __unicode__(self):
        return self.raw_message + " object"
    
    def __str__(self):
        return self.raw_message +" object"
    
        class Admin:
            pass
        
        class Meta:
            pass