from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
#from mysite.core import views as core_views

app_name = 'wall'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^home/$', views.IndexView.as_view(), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'wall/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '../login'}, name='logout'),
    url(r'^new_post/$', views.post, name='new_post')
    ]
