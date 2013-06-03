from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^groups/$','groups.views.list_groups'),
                       (r'^groups/new$','groups.views.new'),  # to create a group
                       (r'^groups/add/$','groups.views.add'),  # post after create
                       (r'^groups/(?P<group_id>\d+)','groups.views.show'),
                       (r'^groups/edit/(?P<group_id>\d+)','groups.views.edit'), # to choose a group to edit
                       (r'^groups/update/(?P<group_id>\d+)','groups.views.update'), # to handle after form is posted for edit
                       (r'^groups/delete/(?P<group_id>\d+)','groups.views.delete'),
    # Examples:
    # url(r'^$', 'Pachondi.views.home', name='home'),
    # url(r'^Pachondi/', include('Pachondi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
