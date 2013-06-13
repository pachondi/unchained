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
        'discussions/group_discussion_form.html',
        {
         'action':'create',
         'button':'Create',
         'link_pk':request.GET.get('link_pk')
        }
    )


# POST /discussion
def create(request):
    if request.method != "POST":
        return redirect('discussions.views.new')
    
    if not request.POST.get("link_pk"):
        return redirect('discussions.views.new')

    params = {}
    name = request.POST["name"]
    group = Group.objects.get(id=request.POST.get("link_pk"))
    params["name"] = name
    params["group"] = group
    group_discussion = GroupDiscussion(**params)     
    group_discussion.save()
    return index(request,"Group Discussion Created")
