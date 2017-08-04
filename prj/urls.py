from django.conf.urls import include, url
from django.contrib import admin
from openrave import views as openrave_views
urlpatterns = [
    # Examples:
    url(r'^$', openrave_views.index),
    url(r'^info.json$', openrave_views.info),
    url(r'^add/(?P<robot_name>\w*)$', openrave_views.add),
    url(r'^remove/(?P<robot_name>\w*)$', openrave_views.remove),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
