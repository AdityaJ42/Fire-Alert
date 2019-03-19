from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^register/$', views.register, name='register'),
	url(r'^volunteers/$', views.show_volunteers, name='all_volunteers'),
	url(r'^directions/(?P<pk>[0-9]+)$', views.directions, name='directions'),
	url(r'^centres/$', views.centres, name='centres'),
	url(r'^safety/$', views.safety, name='safety'),
	url(r'^markers/$', views.markers, name='markers'),
	url(r'^directions2/(?P<pk>[0-9]+)$', views.directions2, name='directions2')
]
