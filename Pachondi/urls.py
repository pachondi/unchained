from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
# [:index, :show, :new, :create, :edit, :update, :destroy] 
urlpatterns = patterns('groups.views',
                       (r'^groups/$','index'), # show all group
                       (r'^groups/new$','new'),  # to create a group
                       (r'^groups/create/$','create'),  # post after create
                       (r'^groups/(?P<group_id>\d+)','show'),
                       (r'^groups/edit/(?P<group_id>\d+)','edit'), # to edit a group
                       (r'^groups/update/(?P<group_id>\d+)','update'), # post after edit
                       (r'^groups/delete/(?P<group_id>\d+)','delete'), # to delete a group
                       (r'^groups/destroy/(?P<group_id>\d+)','destroy'), # to post after delete
                       #(r'^groups*','index'), # catch all, defaults to index
    # Examples:
    # url(r'^$', 'Pachondi.views.home', name='home'),
    # url(r'^Pachondi/', include('Pachondi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
