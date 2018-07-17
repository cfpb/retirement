from django.conf.urls import url

from retirement_api.views import about, claiming, estimator


app_name = 'retirement_api'


urlpatterns = [
    url(r'^before-you-claim/about/$', about, name='about'),
    url(r'^before-you-claim/about/es/$', about, {'language': 'es'},
        name='about_es'),
    url(r'^before-you-claim/$', claiming, name='claiming'),
    url(r'^before-you-claim/es/$', claiming, {'es': True}, name='claiming_es'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$',
        estimator, name='estimator'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/es/$',
        estimator, {'language': 'es'}, name='estimator_es'),
]
