from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='scanner.home'),
    url(r'^new$', views.newscan, name='scanner.newscan'),
    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='scanner.logout'),
    url(r'^bleach/?$', views.bleach_test, name='scanner.bleach'),
)
