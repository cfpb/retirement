from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^retirement-api/estimator/$', 'retirement_api.views.estimator', name='estimator'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'retirement_api.views.estimator', name='estimator'),
    url(r'^retirement-api/get-retirement-age/(?P<birth_year>\d+)/$', 'retirement_api.views.get_full_retirement_age', name='get_full_retirement_age'),
)
