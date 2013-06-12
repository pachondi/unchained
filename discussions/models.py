from django.db import models
from groups.models import Group

# Abstract discussion class.
class Discussion(models.Model):
    pass

    class Meta:
        abstract = True
        
class GroupDiscussion(Discussion):
    name = models.CharField(max_length=30)
    group = models.ForeignKey(Group)
        
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    