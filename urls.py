from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', 'views.main_page'),
    (r'^main_page', 'views.main_page'),
    (r'^index', 'views.index'),
    (r'^user_creation/', 'views.smart_teacher_user_creation'),
    (r'^login/', 'views.smart_teacher_login'),
    (r'^logout/', 'views.smart_teacher_logout'),
    (r'^events/', 'views.events'),
    (r'^donate/', 'views.donate'),
    (r'^help/', 'views.help'),
    (r'^about/', 'views.about'),
    (r'^contact/', 'views.contact'),
    (r'^question/', 'views.question'),
    (r'^pdf/', 'views.pdf'),
    (r'^trial/', 'views.trial'),
    (r'^trial_pdf', 'views.trial_pdf'),
    (r'^sheet/', include('sheet.urls')),
    (r'^smartqands/', include('smartqands.urls')),
)
urlpatterns += staticfiles_urlpatterns()
