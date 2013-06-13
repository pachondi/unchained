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
    
    def __unicode__(self):
        return self.raw_message
    
    def __str__(self):
        return self.raw_message