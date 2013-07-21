from django.forms import ModelForm
from groups.models import Group


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = [ field.name for field in Group.get_editable_fields(Group()) ]
        #fields = ["name","description"]
        '''
        fields = "__all__" # all fields (ommitting will do the same in 1.6)
        exclude = [] # list of all fields  same as above
         if you set editable=False on the model field, any form created 
         from the model via ModelForm will not include that field.
        '''