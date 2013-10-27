from django.db import models

class CountryManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)
    
class Country(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=6)
    objects = CountryManager()    
    
    class Meta:
        unique_together= (('code'),)       
    
    def __unicode__(self):
        return self.name
    
    def natural_key(self):
        return (self.code,)
    
class State(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=6)
    
    def __unicode__(self):
        return self.name