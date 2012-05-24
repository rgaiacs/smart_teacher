from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('smartqands.views',
    (r'^$', 'list_smartqands'),
    (r'^new', 'edit_smartqands'),
    (r'^(?P<smartqands_id>\d+)/$', 'show_smartqands'),
    (r'^(?P<smartqands_description>\w{1,255})/$', 'show_smartqands'),
    (r'^(?P<smartqands_id>\d+)/edit(?P<show>\d+)', 'edit_smartqands'),
    (r'^(?P<smartqands_description>\w{1,255})/edit(?P<show>\d+)', 'edit_smartqands'),
    (r'^(?P<smartqands_id>\d+)/del', 'del_smartqands'),
    (r'^(?P<smartqands_description>\w{1,255})/del', 'del_smartqands'),
    (r'^(?P<smartqands_id>\d+)/history', 'history'),
    (r'^(?P<smartqands_description>\w{1,255})/history', 'history'),
    (r'^(?P<smartqands_id>\d+)/comment/$', 'show_comment'),
    (r'^(?P<smartqands_description>\w{1,128})/comment/$', 'show_comment'),
    (r'^(?P<smartqands_id>\d+)/comment/edit', 'edit_comment'),
    (r'^(?P<smartqands_description>\w{1,128})/comment/edit', 'edit_comment'),
)
