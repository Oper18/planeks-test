# coding: utf-8

import csv
import os
import time

from planeks_test.celery import app

from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Dummy, Report

User = get_user_model()

@app.task
def make_csv_task(user, reportname):
    user = User.objects.get(pk=user)
    report = Report.objects.create(owner=user,
                                   report=reportname)
    time.sleep(20)
    dummy_data = Dummy.objects.filter(owner=user)
    if dummy_data.exists():
        export_data = []
        for d in dummy_data:
            inner_dict = {'name': '{} {}'.format(d.first_name, d.last_name),
                          'job': d.job if d.job else '',
                          'type': d.rec_type if d.rec_type else '',
                          'website': d.website if d.website else '',
                          'date': d.creation_date.isoformat() if d.creation_date else '',
                          'info': d.info if d.info else ''}
            export_data.append(inner_dict)
        fieldnames = export_data[0].keys()
        with open(os.path.join(settings.MEDIA_ROOT, reportname), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in export_data:
                writer.writerow(row)
        report.status = Report.FINISH
        report.save()
