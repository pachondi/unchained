# Create your views here.
from discussions.models import Group, GroupDiscussion
from django.shortcuts import render_to_response, redirect

# Create your views here.

# GET /discussions
def index(request, message=""):
    group_discussion_list = GroupDiscussion.objects.all()
    return render_to_response(
        'discussions/list.html',
        {'group_discussion_list':group_discussion_list,'message':message}
    )


# GET /discussions/new
def new(request):
    return render_to_response(
        'discussions/form.html',
        {
         'action':'create',
         'button':'Create'
        }
    )


# POST /discussion
def create(request):
    if request.method != "POST":
        return redirect('discussions.views.new')
    
    name = request.POST["name"]
    group = Group.objects.get(id=request.POST["group"])
    group_discussion = GroupDiscussion(
                 name = name,
                 group = group      
            )
    group_discussion.save()
    return index(request,"Group Created")
