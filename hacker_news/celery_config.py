from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hacker_news.settings")
config = os.environ.get("DJANGO_CONFIGURATION")
if not config:
  os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

import configurations  # noqa: E402

configurations.setup()

app = Celery("hacker_news")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()