from django.conf.urls import patterns, include, url
from groups.views import GroupDetailView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
# [:index, :show, :new, :create, :edit, :update, :destroy] 
urlpatterns = patterns('groups.views',
                       (r'^groups/$','index'), # show all group
                       (r'^groups/new$','new'),  # to create a group
                       (r'^groups/create/$','create'),  # post after create
                       (r'^groups/(?P<group_id>\d+)/edit','edit'), # to edit a group
                       #(r'^groups/edit/(?P<group_id>\d+)','edit'), # to edit a group
                       (r'^groups/(?P<group_id>\d+)/update','update'), # post after edit
                       #(r'^groups/update/(?P<group_id>\d+)','update'), # post after edit
                       (r'^groups/(?P<group_id>\d+)/delete','delete'), # to delete a group
                       #(r'^groups/delete/(?P<group_id>\d+)','delete'), # to delete a group
                       (r'^groups/(?P<group_id>\d+)/destroy','destroy'), # to post after delete
                       #(r'^groups/destroy/(?P<group_id>\d+)','destroy'), # to post after delete
                       #(r'^groups/(?P<group_id>\d+)','show'),
                       (r'^groups/(?P<pk>\d+)',GroupDetailView.as_view(),None,'show-group')
)

urlpatterns += patterns('discussions.views',
                        (r'group_discussions$','index'),
                        (r'group_discussions/new$','new',None,'new-group-discussion'),
                        (r'group_discussions/create/$','create'),
                        (r'group_discussions/(?P<discussion_id>\d+)/edit','edit',None,'edit-group-discussion'),
                        (r'group_discussions/(?P<discussion_id>\d+)/update','update',None,'update-group-discussion'),
)


urlpatterns += patterns('messages.views',
                        (r'group_discussion_messages/$','index'),
                        (r'group_discussion_messages/new$','new',None,'new-group-discussion-message'),
                        (r'group_discussion_messages/create/$','create',None,'create-group-discussion-message'),
                        (r'group_discussion_messages/(?P<message_id>\d+)/edit','edit',None,'edit-group-discussion-message'), # 
                        (r'group_discussion_messages/(?P<message_id>\d+)/update','update',None,'update-group-discussion-message'), 
                        
                        #(r'group_discussions/(?P<pk>\d+)','show'),
)

"""
https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/#other-helpers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
"""

#(r'^groups*','index'), # catch all, defaults to index
    # Examples:
    # url(r'^$', 'Pachondi.views.home', name='home'),
    # url(r'^Pachondi/', include('Pachondi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

