from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openrave.views.index'),
    url(r'^add/(?P<robot_name>\w*)$', 'openrave.views.add'),
    url(r'^remove/(?P<robot_name>\w*)$', 'openrave.views.remove'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
