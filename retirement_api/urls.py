from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^retirement-api/admin/', include(admin.site.urls)),
    url(r'^before-you-claim/about/$', 'retirement_api.views.about', name='about'),
    url(r'^before-you-claim/about/es/$', 'retirement_api.views.about', {'language': 'es'}, name='about_es'),
    url(r'^before-you-claim/$', 'retirement_api.views.claiming', name='claiming'),
    url(r'^before-you-claim/es/$', 'retirement_api.views.claiming', {'es': True}, name='claiming_es'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'retirement_api.views.estimator', name='estimator'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$', 'retirement_api.views.estimator', {'language': 'es'}, name='estimator_es'),
    url(r'^retirement/retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'retirement_api.views.estimator', name='estimator'),
    url(r'^retirement/retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$', 'retirement_api.views.estimator', {'language': 'es'}, name='estimator_es'),
)

urlpatterns += staticfiles_urlpatterns()
