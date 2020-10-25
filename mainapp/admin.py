# coding: utf-8

from django.contrib import admin

from .models import Dummy, Report


class DummyAdmin(admin.ModelAdmin):
    list_display = ['id', 'job']

admin.site.register(Dummy, DummyAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(Report, ReportAdmin)
