# Create your views here.
from django.shortcuts import render_to_response, redirect
from messages.models import GroupDiscussionMessage
from discussions.models import GroupDiscussion


def index(request, message=""):
    group_disc_msgs_list = GroupDiscussionMessage.objects.all()
    return render_to_response(
        'messages/group_disc_msgs_list.html',
        {'group_disc_msgs_list':group_disc_msgs_list,'message':message}
    )
    
# GET /discussions/new
def new(request):
    return render_to_response(
        'messages/group_disc_msg_form.html',
        {
         'action':'create',
         'button':'Create',
         'link_pk':request.GET.get('link_pk')
        }
    )


# POST /discussion
def create(request):
    if request.method != "POST":
        return redirect('messages.views.new')
    
    if not request.POST.get("link_pk"):
        return redirect('messages.views.new')

    params = {}
    raw_message = request.POST["raw_message"]
    group_disc = GroupDiscussion.objects.get(id=request.POST.get("link_pk"))
    params["raw_message"] = raw_message
    params["group_discussion"] = group_disc
    group_discussion_msg = GroupDiscussionMessage(**params)     
    group_discussion_msg.save()
    return index(request,"Group Discussion Message Created")