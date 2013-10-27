from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from users.forms import UserCreationForm, UserProfileForm, UserSettingsForm
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from users.models import SiteUser, NotificationType, UserSettings, UserNotification, UserPost, PostComment, ConnectionRequest
from django.contrib.auth import authenticate, logout
from django.utils.datetime_safe import datetime
from django.core.exceptions import ObjectDoesNotExist
from users.utils import get_connection_suggestion

@csrf_protect
def index(request, template_name = 'users/login.html', 
          login_form = AuthenticationForm,
          signup_form = UserCreationForm,
          **kwargs):
    if request.user.is_authenticated():
        return redirect('/users/home', **kwargs)    
    
    return render_to_response(template_name, 
                               {'login_form' : login_form, 'signup_form' : signup_form},
                        context_instance=RequestContext(request))

@login_required
def home(request, template_name):
    user = get_object_or_404(SiteUser, id=request.user.id)
    suggested_connections = get_connection_suggestion(user)    
    connections = user.connections.all()
    connection_requests=()
    try:
        connection_requests=ConnectionRequest.objects.filter(to_user=user,status='R')
    except ObjectDoesNotExist:
        print("No connection request for user.")
        
    posts=UserPost.objects.filter(user__in=list(connections)).order_by('-post_dt')
    return render_to_response(template_name, {'posts':posts,
                                              'connections':connections,
                                              'connection_requests':connection_requests,
                                              'suggested_connections':suggested_connections,
                                              'user':user }, 
                              context_instance=RequestContext(request))
          
@csrf_protect
def custom_login(request, template_name = 'users/login.html', **kwargs):
    if request.user.is_authenticated():
        return redirect('/users/settings', **kwargs)
    else:        
        return login(request, template_name, **kwargs)
    
def custom_logout(request, template_name, **kwargs):
    logout(request)
    return redirect('/users/', **kwargs)

@csrf_protect
def signup(request, template_name='users/signup_form.html', 
           email_template_name='users/signup_email.html',
           signup_form=UserCreationForm,
           token_generator=default_token_generator,
           post_signup_redirect=None):
    
    if request.user.is_authenticated():
        return redirect('/users/home')
    
    if post_signup_redirect is None:
        post_signup_redirect = reverse('users.views.home')
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():                            
                opts = {}
                opts['use_https'] = request.is_secure()
                opts['token_generator'] = token_generator
                opts['email_template_name'] = email_template_name
                #if not Site._meta.installed:
                opts['domain_override'] = get_current_site(request).domain
                user = form.save(**opts)   
                user = authenticate(username=user.username,password=user.password)
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # Redirect to a success page.
                        #else:
                        # Return a 'disabled account' error message
                
                return HttpResponseRedirect(post_signup_redirect)
    else:
        form = signup_form()
    return render_to_response(template_name, {'form': form,}, 
                              context_instance=RequestContext(request))

def signup_done(request, template_name='users/signup_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))

def signup_confirm(request, uidb36=None, token=None,
                   token_generator=default_token_generator,
                   post_signup_redirect=None):
    assert uidb36 is not None and token is not None #checked par url
    if post_signup_redirect is None:
        post_signup_redirect = reverse('users.views.settings')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(SiteUser, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.is_verified = True
        user.save()
    else:
        context_instance['validlink'] = False
    return HttpResponseRedirect(post_signup_redirect, {'user': user})

def signup_complete(request, template_name='users/signup_complete.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request, 
                                                              {'login_url': settings.LOGIN_URL}))

@login_required
def profile(request, template_name='users/profile.html'):
    user = get_object_or_404(SiteUser, id=request.user.id)
    post_signup_redirect = reverse('users.views.settings')
            
    try:
        instance = UserSettings.objects.get(pk=user.id)
    except UserSettings.DoesNotExist:
        instance = UserSettings()
        
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():                            
            opts = {}
            opts['user']=user                            
            form.save(**opts)
            return HttpResponseRedirect(post_signup_redirect)            
    else:        
        form = UserProfileForm(instance=instance)
    return render_to_response(template_name, {'form':form,'user': user}, 
                              context_instance=RequestContext(request))
    
@login_required
def view_profile(request, userslug, template_name='users/view_profile.html', **kwargs):
    user = get_object_or_404(SiteUser, user_slug=userslug)
    current_user=get_object_or_404(SiteUser, id=request.user.id)
    connections = user.connections.all()
    posts=UserPost.objects.filter(user__in=list(connections)).order_by('-post_dt')
    add_user=False
    
    if user.id != current_user.id:
        if not current_user.connections.filter(id=user.id):        
            add_user=True
    return render_to_response(template_name, {'posts':posts,
                                              'connections':connections,
                                              'add_user':add_user,
                                              'user':user }, 
                              context_instance=RequestContext(request))          
    
@login_required
def add_post(request, user_id, **kwargs):
    if request.method == "POST":   
        current_user = get_object_or_404(SiteUser, id=request.user.id)
        user = get_object_or_404(SiteUser, id=user_id)
        post = UserPost()
        post.user=current_user
        post.message=request.POST["message"]
        post.post_by=user
        post.post_dt=datetime.now();
        post.save()
    
    return redirect('/users/home', **kwargs)

@login_required
def delete_post(request, post_id, **kwargs):    
    post = UserPost.objects.get(pk=post_id)
    post.delete()
    
    return redirect('/users/home', **kwargs)

@login_required
def post_comment(request, post_id, **kwargs):
    if request.method == "POST":   
        user = get_object_or_404(SiteUser, id=request.user.id)
        post = UserPost.objects.get(pk=post_id)
        comment=PostComment()
        comment.post=post
        comment.comment_by=user
        comment.message=request.POST["comment"]
        comment.save()
    
    return redirect('/users/home', **kwargs)

@login_required
def delete_comment(request, comment_id, **kwargs):    
    comment = PostComment.objects.get(pk=comment_id)        
    if comment:
        comment.delete()
    
    return redirect('/users/home', **kwargs)

@login_required
def request_connect(request, uid, **kwargs):    
    from_user =SiteUser.objects.get(pk=request.user.id)
    to_user = SiteUser.objects.get(pk=uid)
    connection_request=ConnectionRequest()
    connection_request.from_user=from_user
    connection_request.to_user=to_user
    connection_request.status='R'
    connection_request.save()
    
    return redirect('/users/home', **kwargs)

@login_required
def confirm_connect(request, uid, **kwargs):    
    to_user =SiteUser.objects.get(pk=request.user.id)
    from_user = SiteUser.objects.get(pk=uid)
    connection_request=ConnectionRequest.objects.get(from_user=from_user,to_user=to_user)    
    connection_request.status='A'
    connection_request.save()
    to_user.connections.add(from_user)
    to_user.save()
    
    return redirect('/users/home', **kwargs)

@login_required
def decline_connect(request, uid, **kwargs):    
    to_user =SiteUser.objects.get(pk=request.user.id)
    from_user = SiteUser.objects.get(pk=uid)
    connection_request=ConnectionRequest.objects.get(from_user=from_user,to_user=to_user)    
    connection_request.status='D'    
    connection_request.save()
    
    return redirect('/users/home', **kwargs)

@login_required    
def settings(request, template_name='users/settings.html',settings_form=UserSettingsForm):
    user = get_object_or_404(SiteUser, id=request.user.id)        
    try:
        instance = UserSettings.objects.get(pk=user.id)
    except UserSettings.DoesNotExist:
        instance = UserSettings()
        
    if request.method == "POST":        
        form = settings_form(request.POST, instance=instance)
        if form.is_valid():
            opts = {}
            opts['user']=user
            form.save(**opts)            
    else:
        form = settings_form(instance=instance)
        
    return render_to_response(template_name, {'user': user, 'form':form, 'notifications':instance.get_notification_settings()}, 
                              context_instance=RequestContext(request))

@login_required    
def notificationsettings(request, template_name='users/settings.html',settings_form=UserSettingsForm):
    user = get_object_or_404(SiteUser, id=request.user.id)
    try:
        instance = UserSettings.objects.get(pk=user.id)
    except UserSettings.DoesNotExist:
        instance = UserSettings()
        
    post_redirect = reverse('users.views.settings')
    
    selected_notifications = request.POST.getlist('notification')
    default_notifications = NotificationType.objects.all()
    
    for notification in default_notifications:
        if str(notification.id) in selected_notifications:
            notification.is_default_enabled = True
        else:
            notification.is_default_enabled = False
      
    instance.set_notification_settings(default_notifications)
    
    return redirect(post_redirect)

