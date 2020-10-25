# coding: utf-8

from django.urls import re_path

from .views import PlaneksView, planeks_login, planeks_logout, make_csv, check_report, add_record

urlpatterns = [
    re_path(r'^$', PlaneksView.as_view(template_name='mainapp/index.html'), name='index'),
    re_path(r'^ajax/login/$', planeks_login, name='ajax_login'),
    re_path(r'^ajax/logout/$', planeks_logout, name='ajax_logout'),
    re_path(r'^ajax/make_csv/$', make_csv, name='ajax_csv'),
    re_path(r'^ajax/check_report_status/$', check_report, name='ajax_checker'),
    re_path(r'^ajax/add_record/$', add_record, name='ajax_add_record'),
]