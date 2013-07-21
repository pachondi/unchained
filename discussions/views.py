# Create your views here.
from discussions.models import Group, GroupDiscussion
from django.shortcuts import render_to_response, redirect
# from django.template import RequestContext

# Create your views here.

# GET /discussions
def index(request, message=""):
    group_discussion_list = GroupDiscussion.objects.all()
    return render_to_response(
        'discussions/list.html'
        ,{'group_discussion_list':group_discussion_list,'message':message}
        #,context_instance=RequestContext(request) # no need to do this is using Generic View
        # http://stackoverflow.com/questions/10355194/how-to-serve-static-files-for-local-development-in-django-1-4
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

def show(request,pk):
    groupdiscussion = GroupDiscussion.objects.get(id=pk)
    return render_to_response(
        'discussions/group_discussion_detail.html',
        {
         'GroupDiscussion':groupdiscussion,
         'link_pk':pk
        }
    )
