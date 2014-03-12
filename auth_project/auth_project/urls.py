from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from login import views as login_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auth_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login_views.user_login),
    url(r'^logout/$', login_views.user_logout),
    url(r'^register/$', login_views.user_register),
    url(r'^validate/$', login_views.user_validate),
    url(r'^$', login_views.home),
)
