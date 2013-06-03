# Create your views here.
from groups.models import Group
from django.template import Context, loader
from django.shortcuts import render_to_response


def list(request, message=""):
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
    
def add(request):
    group_name=request.POST["group_name"]
    group_description=request.POST["group_description"]
    group = Group(
                 group_name = group_name,
                 group_description = group_description      
            )
    group.save()
    return list(request,"Group Created")

#def groups_home(request):
    #html = "<html><body>Testing</body></html>"
    #return HttpResponse(html)
    
