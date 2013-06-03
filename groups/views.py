# Create your views here.
from groups.models import Group
# from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse

def list_groups(request, message=""):
    group_list = Group.objects.all()
    return render_to_response(
        'groups/list.html',
        {'group_list':group_list,'message':message}
    )

def new(request):
    return render_to_response(
        'groups/form.html',
        {
         'action':'add',
         'button':'Create'
        }
    )

def show(request, group_id):
    group = Group.objects.get(id=group_id)
    return render_to_response(
               'groups/form.html',                
               {
                'action':'',
                'button':'',
                'Group':group
                }                   
           )
   
def add(request):
    group_name = request.POST["group_name"]
    group_description = request.POST["group_description"]
    group = Group(
                 group_name = group_name,
                 group_description = group_description      
            )
    group.save()
    return list_groups(request,"Group Created")

def edit(request,group_id):
    group = Group.objects.get(id=group_id)
    return render_to_response(
               'groups/form.html',                
               {
                'action':'update/' + group_id,
                'button':'Update',
                'Group':group
                }                   
           )
 
def update(request,group_id):
    group = Group.objects.get(id=group_id)
    group.group_name = request.POST["group_name"]
    group.group_description = request.POST["group_description"]
    group.save()
    return list_groups(request,message="Group " + group.group_name + " Updated.")   
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)

def delete(request,group_id):
    Group.objects.get(id=group_id).delete()
    return list_groups(request,message="Group Deleted.")

#def groups_home(request):
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)
    
