from django.conf.urls import patterns

urlpatterns = patterns('app.discussions.views',
                        (r'new$','new',None,'new-group-discussion'),
                        (r'create/$','create',None,'create-group-discussion'),
                        (r'(?P<discussion_id>\d+)/edit','edit',None,'edit-group-discussion'),
                        (r'(?P<discussion_id>\d+)/update','update',None,'update-group-discussion'),
                        (r'$','index'),
                       
)