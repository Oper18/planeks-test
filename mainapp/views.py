# coding: utf-8

import re
import uuid
import os

from django.views.generic import TemplateView
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse

from .models import Dummy, Report
from .tasks import make_csv_task


class PlaneksView(TemplateView):

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(csrf(request))
        context = self.get_context_data(request, **kwargs)
        context.update(csrf(request))
        return self.render_to_response(context)

    def get_context_data(self, request, **kwargs):
        context = super(PlaneksView, self).get_context_data()
        if request.user.is_authenticated:
            context['data'] = Dummy.objects.filter(owner=request.user)
        else:
            context['data'] = []
        return context


# @csrf_protect
def planeks_login(request):
    print(csrf(request))
    user = request.POST.get('username')
    password = request.POST.get('password')

    ath = authenticate(request=request, username=user, password=password)
    if ath:
        login(request, ath)
        redir = re.search(r'\?next=.+', request.POST.get('uri')) if request.POST.get('uri') else None
        try:
            redir = redir.group(0).split('=')[-1]
        except Exception as e:
            redir = '/'
        return JsonResponse({'success': True, 'redirect': redir}, status=200)
    else:
        return JsonResponse({'success': False}, status=400)


@csrf_exempt
def planeks_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect': '/'}, status=200)


@csrf_protect
def make_csv(request):
    if request.user.is_authenticated:
        reportname = uuid.uuid4().hex + '.csv'
        make_csv_task.delay(user=request.user.pk, reportname=reportname)
        return JsonResponse({'success': True, 'filename': reportname}, status=200)
    return JsonResponse({'success': False}, status=400)


@csrf_protect
def check_report(request):
    if request.user.is_authenticated:
        print(request.POST.get('filename'))
        report = Report.objects.filter(owner=request.user, report=request.POST.get('filename'))
        if report.exists() and report[0].status == Report.FINISH:
            return JsonResponse({'success': True, 'link': '/media/' + os.path.split(report[0].report.path)[-1]}, status=200)
    return JsonResponse({'success': False}, status=400)


@csrf_protect
def add_record(request):
    if request.user.is_authenticated:
        Dummy.objects.create(owner=request.user,
                             first_name=request.POST.get('first_name', None),
                             last_name=request.POST.get('last_name', None),
                             job=request.POST.get('job', None),
                             rec_type=request.POST.get('type', Dummy.ONE),
                             website=request.POST.get('website', None),
                             creation_date=request.POST.get('creation_date', None),
                             info=request.POST.get('info', None))
        return JsonResponse({'success': True}, status=200)
    return JsonResponse({'success': False}, status=400)
