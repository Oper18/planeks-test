# coding: utf-8

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Dummy(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    RECORD_TYPE = (
        (ONE, 'type one'),
        (TWO, 'type two'),
        (THREE, 'type three'),
        (FOUR, 'type four'),
    )
    owner = models.ForeignKey(User, verbose_name='Record owner', on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='First name', max_length=64, null=True, blank=True)
    last_name = models.CharField(verbose_name='Last name', max_length=64, null=True, blank=True)
    job = models.CharField(verbose_name='Job', max_length=255, null=True, blank=True)
    rec_type = models.PositiveSmallIntegerField(verbose_name='Some type', choices=RECORD_TYPE, default=ONE, blank=True)
    website = models.CharField(verbose_name='Rec link', max_length=255, null=True, blank=True)
    creation_date = models.DateField(verbose_name='Date of creation', null=True, blank=True)
    info = models.TextField(verbose_name='Some info', null=True, blank=True)


class Report(models.Model):
    WAIT = 0
    FINISH = 1
    FAIL = 2
    STATUS = (
        (WAIT, 'waiting'),
        (FINISH, 'finished'),
        (FAIL, 'failed'),
    )

    owner = models.ForeignKey(User, verbose_name='Report owner', on_delete=models.CASCADE)
    report = models.FileField(upload_to='reports', null=True)
    status = models.PositiveSmallIntegerField(verbose_name='Status', choices=STATUS, default=WAIT, blank=True)
    created_at = models.DateTimeField(verbose_name='Created date', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated date', auto_now=True)
