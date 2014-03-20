from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from login import views as login_views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'auth_project.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', login_views.UserLogin.as_view(), name='user_login'),
                       url(r'^logout/$', login_views.UserLogout.as_view(), name='user_logout'),
                       url(r'^register/$', login_views.UserRegister.as_view(), name='user_register'),
                       url(r'^validate/$', login_views.UserValidate.as_view(), name='user_validate'),
                       url(r'^reset_pw_email/$', login_views.PWResetEmail.as_view(), name='reset_pw_email'),
                       url(r'^reset_pw_response/$', login_views.PWResetResponse.as_view(), name='reset_pw_response'),
                       url(r'^$', login_views.HomeView.as_view(), name='user_home'),
)
