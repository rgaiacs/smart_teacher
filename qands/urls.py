from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('qands',
    (r'^$', 'views.index'),
    (r'^logout/', 'views.logout'),
    (r'^question/', 'views.question'),
    (r'^pdf/', 'views.pdf'),
    (r'^sheet/', include('sheet.urls')),
)
