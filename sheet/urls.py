from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sheet.views',
    (r'^(?P<sheet_filter>\w{3})/$', 'list_sheets'),
    (r'^new', 'edit_sheet'),
    (r'^(?P<sheet_id>\d+)/$', 'show_sheet'),
    (r'^(?P<sheet_id>\d+)/edit', 'edit_sheet'),
    (r'^(?P<sheet_id>\d+)/del/$', 'del_sheet'),
    (r'^(?P<sheet_id>\d+)/del/(?P<id_qands>\d+)/$', 'del_qands_from_sheet'),
    (r'^(?P<sheet_id>\d+)/add_question/$', 'list_smartqands'),
    (r'^(?P<sheet_id>\d+)/add_question/(?P<smartqands_id>\d+)', 'smartqands_to_qands'),
    (r'^(?P<sheet_id>\d+)/(?P<id_qands>\d+)/$', 'show_qands_from_sheet'),
    (r'^(?P<sheet_id>\d+)/pdf', 'export_pdf'),
)
