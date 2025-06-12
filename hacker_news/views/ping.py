import os

from django.http import HttpRequest, JsonResponse


def ping(request: HttpRequest) -> JsonResponse:
  env = os.environ.get("DJANGO_CONFIGURATION", "Local")
  return JsonResponse({"success": True, "env": env})
