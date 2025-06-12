from typing import Any

from django.http import HttpRequest


class ReadOnlyAdminMixin:
  def has_add_permission(self, request: HttpRequest) -> bool:
    return False

  def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:  # noqa: ANN401
    return False

  def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:  # noqa: ANN401
    return False
