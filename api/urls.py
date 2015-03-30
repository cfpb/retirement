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
    url(r'^retire-api/get_fra/$', 'api.views.get_fra', name='get_fra'),

)
