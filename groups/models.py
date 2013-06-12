from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def get_detail_fields(self):
        return dict([(field.name,self._get_FIELD_display(field)) for field in self.__class__._meta.fields])
     
    def get_group_discussions(self):
        # Get related discussions for this group. Thanks to
        # http://stackoverflow.com/questions/4611340/an-issue-filtering-related-models-inside-the-model-definition
        return [(group_discussions.id,group_discussions) for group_discussions in self.groupdiscussion_set.all()]
     
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
        class Admin:
            pass
        
        class Meta:
            pass


