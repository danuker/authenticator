from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    url(r'^$', login_views.home),
)
