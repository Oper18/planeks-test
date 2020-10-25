#!/bin/bash

gunicorn -b 0.0.0.0:8000 --access-logfile - --error-logfile - planeks.wsgi &
celery -A planeks_test worker -l info -B
