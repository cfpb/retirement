from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

try:
    STANDALONE = settings.STANDALONE
except AttributeError:  # pragma: no cover
    STANDALONE = False

urlpatterns = [
    url(r'^before-you-claim/about/$', 'retirement_api.views.about',
        name='retirement_about'),
    url(r'^before-you-claim/about/es/$', 'retirement_api.views.about',
        {'language': 'es'}, name='retirement_about_es'),
    url(r'^before-you-claim/$', 'retirement_api.views.claiming',
        name='claiming'),
    url(r'^before-you-claim/es/$', 'retirement_api.views.claiming',
        {'es': True}, name='claiming_es'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$',
        'retirement_api.views.estimator', name='estimator'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$',
        'retirement_api.views.estimator',
        {'language': 'es'}, name='estimator_es'),
    ]

if STANDALONE:
    admin.autodiscover()
    urlpatterns = [
        url(r'^retirement/admin/', include(admin.site.urls)),
        url(r'^retirement/before-you-claim/about/$',
            'retirement_api.views.about', name='retirement_about'),
        url(r'^retirement/before-you-claim/about/es/$',
            'retirement_api.views.about',
            {'language': 'es'}, name='retirement_about_es'),
        url(r'^retirement/before-you-claim/$',
            'retirement_api.views.claiming', name='claiming'),
        url(r'^retirement/before-you-claim/es/$',
            'retirement_api.views.claiming', {'es': True}, name='claiming_es'),
        url(r'^retirement/retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$',
            'retirement_api.views.estimator', name='estimator'),
        url(r'^retirement/retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$',
            'retirement_api.views.estimator',
            {'language': 'es'}, name='estimator_es'),
        ]