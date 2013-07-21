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
        

    def get_discussions_for_parent(self,g_id):
        return [ (discussion.id, discussion.name) for discussion in self.objects.filter(group=g_id) ]  
    
    def __unicode__(self):
        return self.name+ " object"
    
    def __str__(self):
        return self.name+" object"

        class Admin:
            pass
        
        class Meta:
            pass