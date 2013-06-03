from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=30)
    group_description = models.CharField(max_length=100)
    
    class Admin:
        pass
    
    def __str__(self):
        return self.group_name