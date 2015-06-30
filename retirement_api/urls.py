from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'retirement_api.views.estimator', name='estimator'),
    # url(r'^retirement/retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'retirement_api.views.estimator', name='estimator'),
    url(r'^retirement-api/get-retirement-age/(?P<birth_year>\d+)/$', 'retirement_api.views.get_full_retirement_age', name='get_full_retirement_age'),
    url(r'^claiming-social-security/$', 'retirement_api.views.claiming', name='claiming'),
    url(r'^claiming-social-security/es/$', 'retirement_api.views.claiming', {'es': True}),
    url(r'^retirement/static\/(?P<path>.*)/$', 'django.contrib.staticfiles.views.serve')
)

urlpatterns += staticfiles_urlpatterns()
