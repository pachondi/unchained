from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=30)
    group_description = models.CharField(max_length=100)
    
    def get_detail_fields(self):
        return dict([(field.name,self._get_FIELD_display(field)) for field in self.__class__._meta.fields])
        
    def __unicode__(self):
        return self.group_name
    
    def __str__(self):
        return self.group_name
    
        class Admin:
            pass
        
        class Meta:
            pass


