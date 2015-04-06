from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),  
    # url(r'^retire-api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^retire-api/estimator/$', 'api.views.estimator', name='estimator'),
    url(r'^retire-api/estimator/(?P<dob>[^/]+)/(?P<income>\d+)/$', 'api.views.estimator', name='estimator'),
    url(r'^retire-api/get_retirement_age/(?P<birth_year>\d+)/$', 'api.views.get_full_retirement_age', name='get_full_retirement_age'),

)
