import logging
log = logging.getLogger(__name__)
from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    
    def get_object_data(self):
        return dict([(field.name,self._get_FIELD_display(field)) for field in self.__class__._meta.fields])
    
    def get_editable_fields(self):
        return [field for field in self.__class__._meta.fields]
     
    def get_group_discussions(self, discussion_id=None):
        # Get related discussions for this group. Thanks to
        # http://stackoverflow.com/questions/4611340/an-issue-filtering-related-models-inside-the-model-definition
        return [(group_discussions.id,group_discussions) for group_discussions in self.groupdiscussion_set.all()]
         
    def get_messages_for_discussions(self,message_id=None):
        """
        data is returned as array of messages for each discussion
        possibly a json dumps needs to be done for async
        requests. So need a common function that dumps 
        a. json object, b. xml
        """
        displayable_discussions = self.get_group_discussions()
        
        for i in range(len(displayable_discussions)):
            #displayable_messages =  gobj.groupdiscussionmessage_set.all()
            disc_id, disc_obj  = displayable_discussions[i]
            message_list = disc_obj.groupdiscussionmessage_set.all()
            displayable_discussions[i] = (disc_id, disc_obj, message_list)
        
        return displayable_discussions    
    
    def get_group_discussions_with_messages(self):
        """
        properties of self.groupdiscussion_set
         __class__, __delattr__, __dict__, __doc__, __format__, __getattribute__, __hash__, __init__,
          __module__, __new__, __reduce__, __reduce_ex__, __repr__, __setattr__, __sizeof__, __str__,
         __subclasshook__  __weakref__  _copy_to_model  _db  _inherited  _insert  _set_creation_counter
         _update  add  aggregate all  annotate  bulk_create complex_filter contribute_to_class
         core_filters count create creation_counter dates  db db_manager defer distinct exclude
         exists  extra  filter get get_empty_query_set get_or_create 
         get_prefetch_query_set get_query_set in_bulk  instance
         iterator latest model none only order_by prefetch_related raw reverse
         select_for_update select_related update  using values values_list        
        """
        """
         _set doesn't 
        """
        rs = [] # create an empty list that will hold the result set
        
        for gd in self.groupdiscussion_set.all():
            irs = (gd,gd.groupdiscussionmessage_set.count())
            # if you don't do this here, 
            # discussions with no messages wont be added
            if gd.groupdiscussionmessage_set.exists() is False:
                #log.debug(gd.groupdiscussionmessage_set.count())
                rs.append(irs) 
            
            for gdm in gd.groupdiscussionmessage_set.all():
                irss = irs + (gdm,) # if messages found for a group
                rs.append(irss) #append the result set to a list.
            
        return rs
        
        #return [(gd_msgs.id,gd_msgs.raw_message,gd_msgs.group_discussion) for gd_msgs in self.groupdiscussion_set.groupdiscussionmessage_set.all()]
    @models.permalink
    def get_absolute_url(self):
        return ('show-group', [str(self.id)])   
        
    def __unicode__(self):
        return self.name + " object"
    
    def __str__(self):
        return self.name + " object"
    
        class Admin:
            pass
        
        class Meta:
            pass


