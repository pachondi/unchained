# Create your views here.
from django.shortcuts import render_to_response, redirect
from messages.models import GroupDiscussionMessage
from discussions.models import GroupDiscussion

import logging
log = logging.getLogger(__name__)


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
         'belongs_to':request.GET.get('belongs_to')
        }
    )


# POST /discussion
def create(request):
    if request.method != "POST":
        return redirect('messages.views.new')
    
    if not request.POST.get("belongs_to"):
        return redirect('messages.views.new')
    
    
    params = {}
    raw_message = request.POST["raw_message"]
    group_disc = GroupDiscussion.objects.get(id=request.POST.get("belongs_to"))
    params["raw_message"] = raw_message
    params["group_discussion"] = group_disc
    group_discussion_msg = GroupDiscussionMessage(**params)
    group_discussion_msg.save()
    
    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view,context_referrer_id)
    
    return index(request,"Group Discussion Message Created")


def edit(request,message_id):
    
    gdm = GroupDiscussionMessage.objects.get(id=message_id)
    
    return render_to_response(
               'messages/group_disc_msg_form.html',                
               {
                                    "mode":"edit",
                                    "button":"Update",
                                    "action":"update",
                                    "action_url":"/group_discussion_messages/"+message_id+"/update",
                                    "message_id":message_id,
                                    "raw_message":gdm.raw_message,
                                    "belongs_to":request.POST.get("belongs_to"),
                                    "context_referrer":request.POST.get("context_referrer"),
                                    "context_referrer_id":request.POST.get("context_referrer_id")
                }                   
           )

#PUT /groups/:id
def update(request,message_id):
    
    gdm = GroupDiscussionMessage.objects.get(id=message_id)
    gdm.raw_message = request.POST["raw_message"]
    gdm.save()

    context_referrer = request.POST.get("context_referrer")
    if context_referrer:
        context_referrer_id = request.POST.get("context_referrer_id")
        context_view = "show-" + context_referrer
        return redirect(context_view,context_referrer_id)
    
    return index(request,"Group Discussion Message Created")
