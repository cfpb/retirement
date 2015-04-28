from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^retirement-api/estimator/$', 'views.estimator', name='estimator'),
    url(r'^retirement-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'views.estimator', name='estimator'),
    url(r'^retirement-api/get-retirement-age/(?P<birth_year>\d+)/$', 'views.get_full_retirement_age', name='get_full_retirement_age'),
)
