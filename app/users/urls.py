from django.conf.urls import patterns
from app.users.views import custom_login, index, home
from django.conf.urls.defaults import include
#from users.api import SiteUserResource

#siteuser_resource = SiteUserResource()

urlpatterns = patterns('',
                       (r'^$', index,{'template_name': 'users/index.html'}),
                       
                       (r'^home/$', home,{'template_name': 'users/home.html'}),
                       
                       (r'^login/$', 
                        custom_login, 
                        {'template_name': 'users/login.html'}),

                       (r'^logout/$', 
                        'app.users.views.custom_logout', 
                        {'template_name': 'users/logged_out.html'}),

                       (r'^password_change/$', 
                        'django.contrib.auth.views.password_change', 
                        {'template_name': 'users/password_change_form.html'}),

                       (r'^password_change/done/$', 
                        'django.contrib.auth.views.password_change_done', 
                        {'template_name': 'users/password_change_done.html'}),

                       (r'^password_reset/$', 
                        'django.contrib.auth.views.password_reset', 
                        {'template_name': 'users/password_reset_form.html',
                         'email_template_name': 'users/password_reset_email.html'}),

                       (r'^password_reset/done/$', 
                        'django.contrib.auth.views.password_reset_done', 
                        {'template_name': 'users/password_reset_done.html'}),

                       (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
                        'django.contrib.auth.views.password_reset_confirm', 
                        {'template_name': 'users/password_reset_confirm.html'}),

                       (r'^reset/done/$', 
                        'django.contrib.auth.views.password_reset_complete', 
                        {'template_name': 'users/password_reset_complete.html'}),

                       (r'^signup/$', 
                        'app.users.views.signup', 
                        {'template_name': 'users/signup_form.html',
                         'email_template_name': 'users/signup_email.html'}),

                       (r'^signup/done/$', 
                        'app.users.views.signup_done', 
                        {'template_name': 'users/signup_done.html'}),

                       (r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
                        'app.users.views.signup_confirm'),

                       (r'^signup/complete/$', 
                        'app.users.views.signup_complete', 
                        {'template_name': 'users/signup_complete.html'}),
                       
                       (r'^profile/$', 
                        'app.users.views.profile', 
                        {'template_name': 'users/profile.html'}),
                       
                       (r'^settings/$', 
                        'app.users.views.settings', 
                        {'template_name': 'users/settings.html'}),
                       
                       (r'^notificationsettings/$', 
                        'app.users.views.notificationsettings', 
                        {'template_name': 'users/settings.html'}),
                       
                       (r'^home/(?P<userslug>([a-zA-Z]*).([a-zA-Z]*).\d+-\d+-\d+)$', 'app.users.views.view_profile'),
                       
                       (r'^post/(?P<user_id>\d+)/add$', 'app.users.views.add_post'),
                       
                       (r'^post/(?P<post_id>\d+)/remove$', 'app.users.views.delete_post'),
                       
                       (r'^post/(?P<post_id>\d+)/comment/add$', 'app.users.views.post_comment'),
                       
                       (r'^post/comment/(?P<comment_id>\d+)/remove$', 'app.users.views.delete_comment'),
                       
                       (r'^request/(?P<uid>\d+)$', 'app.users.views.request_connect'),
                       (r'^accept/(?P<uid>\d+)$', 'app.users.views.confirm_connect'),
                       (r'^reject/(?P<uid>\d+)$', 'app.users.views.decline_connect'),
                       
                       #(r'^api/', include(siteuser_resource.urls)),
)