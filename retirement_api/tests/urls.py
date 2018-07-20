from django.conf.urls import include, url
from django.contrib import admin 

import retirement_api.urls


urlpatterns = [
    url(r'^', include(retirement_api.urls, 'retirement_api')),
    url(r'^admin/', include(admin.site.urls)),
]
