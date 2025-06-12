"""
WSGI config for hacker_news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hacker_news.settings")


config = os.environ.get("DJANGO_CONFIGURATION")
if not config:
  os.environ.setdefault("DJANGO_CONFIGURATION", "Local")


from configurations.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
