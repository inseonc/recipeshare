from django.conf.urls import patterns, include, url
from recipeShareApp.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from recipeShareApp import views


router = routers.DefaultRouter()
router.register(r'test', views.recipeShareApp_view_Set)


admin.autodiscover()
 
urlpatterns = [
    # Examples:
    # url(r'^$', 'timelineproject.views.home', name='home'),
    # url(r'^timelineproject/', include('timelineproject.foo.urls')),
 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
 
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/recipeShareApp/$', recipeShareApp_view),
    url(r'^api/recipeShareApp/(?P<num>\d+)/$', recipeShareApp_view_page),
    url(r'^api/user/(?P<method>create)/$', user_view),
    url(r'^api/user/(?P<method>update)/$', user_view),
    url(r'^api/user/(?P<method>list)/$', user_view),
    #url(r'^api/recipeShareApp/create/$', upload_file),
    url(r'^api/recipeShareApp/create/$', message_create_view),
    url(r'^api/recipeShareApp/(?P<num>\d+)/$', message_view),
    url(r'^api/recipeShareApp/(?P<num>\d+)/delete/$', message_delete_view),
    url(r'^api/recipeShareApp/(?P<num>\d+)/like/$', like_view),
    url(r'^api/recipeShareApp/find/$', find_view),
    url(r'^api/user/name/$', name_view),
    url(r'^api/user/checkpassword/$', checkpassword_view),
    url(r'^api/user/setpassword/$', setpassword_view),
    url(r'^api/profile/(?P<username>\w+)/$', profile_view),
    url(r'^api/profile/$', profile_view),
    url(r'^api/login/$', login_view),
    url(r'^home/(?P<page>\w+).html$', serve_html),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)