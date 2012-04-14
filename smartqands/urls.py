from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('smartqands.views',
    (r'^$', 'list_smartqands'),
    (r'^add_to=(?P<id_sheet>\d+)/$', 'list_smartqands'),
    (r'^new', 'edit_smartqands'),
    (r'^(?P<id_smartqands>\d+)/$', 'show_smartqands'),
    (r'^(?P<id_smartqands>\d+)/edit', 'edit_smartqands'),
    (r'^(?P<id_smartqands>\d+)/del', 'edit_smartqands'),
    (r'^add_to=(?P<id_sheet>\d+)/(?P<id_smartqands>\d+)/$', 'show_smartqands'),
    (r'^add_to=(?P<id_sheet>\d+)/(?P<id_smartqands>\d+)/upload', 'smartqands_to_qands'),
)
