from django.forms import ModelForm
from app.groups.models import Group, GroupType


class GroupForm(ModelForm):
    class Meta:
        model = Group
        exclude = ['created_by']
        #fields = [ field.name for field in Group.get_editable_fields(Group()) ]
        #fields = ["name","description"]
        '''
        fields = "__all__" # all fields (ommitting will do the same in 1.6)
        exclude = [] # list of all fields  same as above
         if you set editable=False on the model field, any form created 
         from the model via ModelForm will not include that field.
        '''
        
    def save(self,user):
        group = super(GroupForm, self).save(commit=False)        
        group.name = self.data["name"]
        group.description = self.data["description"]
        group.website = self.data["website"]
        group.type = GroupType.objects.get(pk=self.data["type"])
        group.created_by=user
        group.save()