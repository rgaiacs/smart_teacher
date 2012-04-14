from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sheet.views',
    (r'^$', 'list_sheets'),
    (r'^new', 'edit_sheet'),
    (r'^(?P<id_sheet>\d+)/$', 'show_sheet'),
    (r'^(?P<id_sheet>\d+)/edit', 'edit_sheet'),
    (r'^(?P<id_sheet>\d+)/del/$', 'del_sheet'),
    (r'^(?P<id_sheet>\d+)/del/(?P<id_qands>\d+)/$', 'del_qands_from_sheet'),
    (r'^(?P<id_sheet>\d+)/(?P<id_qands>\d+)/$', 'show_qands_from_sheet'),
    (r'^(?P<id_sheet>\d+)/pdf', 'export_pdf'),
)
