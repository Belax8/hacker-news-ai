"""
Original Code: https://github.com/mishbahr/django-modeladmin-reorder
Added Admin Sidebar: https://github.com/mishbahr/django-modeladmin-reorder/pull/49/files
"""

from copy import deepcopy

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import Resolver404, resolve
from django.utils.deprecation import MiddlewareMixin


class ModelAdminReorder(MiddlewareMixin):
  def init_config(self, request: HttpRequest, app_list: list) -> None:
    self.request = request
    self.app_list = app_list

    self.config = getattr(settings, "ADMIN_REORDER", None)
    if not self.config:
      # ADMIN_REORDER settings is not defined.
      raise ImproperlyConfigured("ADMIN_REORDER config is not defined.")

    if not isinstance(self.config, (tuple, list)):
      raise ImproperlyConfigured(
        "ADMIN_REORDER config parameter must be tuple or list. Got {config}".format(config=self.config)
      )

    # Flatten all models from apps
    self.models_list = []
    for app in app_list:
      for model in app["models"]:
        model["model_name"] = self.get_model_name(app["app_label"], model["object_name"])
        self.models_list.append(model)

  def get_app_list(self) -> list:
    ordered_app_list = []
    if self.config is not None:
      for app_config in self.config:
        app = self.make_app(app_config)
        if app:
          ordered_app_list.append(app)
    return ordered_app_list

  def make_app(self, app_config: dict | str) -> dict | None:
    if not isinstance(app_config, (dict, str)):
      raise TypeError("ADMIN_REORDER list item must be dict or string. Got %s" % repr(app_config))

    if isinstance(app_config, str):
      # Keep original label and models
      return self.find_app(app_config)
    else:
      return self.process_app(app_config)

  def find_app(self, app_label: str) -> dict | None:
    for app in self.app_list:
      if app["app_label"] == app_label:
        return app
    return None

  def get_model_name(self, app_name: str, model_name: str) -> str:
    if "." not in model_name:
      model_name = "%s.%s" % (app_name, model_name)
    return model_name

  def process_app(self, app_config: dict) -> dict | None:  # noqa: C901
    if "app" not in app_config:
      raise NameError('ADMIN_REORDER list item must define a "app" name. Got %s' % repr(app_config))

    app = self.find_app(app_config["app"])
    if app:
      app = deepcopy(app)
      # Rename app
      if "label" in app_config:
        app["name"] = app_config["label"]

      # Process app models
      if "models" in app_config:
        models_config = app_config.get("models")
        if models_config is not None:
          models = self.process_models(models_config)
          if models:
            app["models"] = models
          else:
            return None
      return app
    return None

  def process_models(self, models_config: list | tuple | dict) -> list:
    if not isinstance(models_config, (dict, list, tuple)):
      raise TypeError(
        '"models" config for ADMIN_REORDER list item must be dict or list/tuple. Got %s' % repr(models_config)
      )

    ordered_models_list = []
    for model_config in models_config:
      model = None
      if isinstance(model_config, dict):
        model = self.process_model(model_config)
      else:
        model = self.find_model(model_config)

      if model:
        ordered_models_list.append(model)

    return ordered_models_list

  def find_model(self, model_name: str) -> dict | None:
    for model in self.models_list:
      if model["model_name"] == model_name:
        return model
    return None

  def process_model(self, model_config: dict) -> dict | None:
    # Process model defined as { model: 'model', 'label': 'label' }
    for key in (
      "model",
      "label",
    ):
      if key not in model_config:
        return None
    model = self.find_model(model_config["model"])
    if model:
      model["name"] = model_config["label"]
      return model
    return None

  def process_template_response(self, request: HttpRequest, response: TemplateResponse) -> TemplateResponse:  # noqa: C901
    try:
      url = resolve(request.path_info)
    except Resolver404:
      return response
    if not url.app_name == "admin" and url.url_name not in ["index", "app_list"]:
      # current view is not a django admin index
      # or app_list view, bail out!
      return response

    if response.context_data is None:
      return response

    if "app_list" in response.context_data:
      app_list = response.context_data["app_list"]
      context_key = "app_list"
      # handle django 3.1 sidebar
    elif "available_apps" in response.context_data:
      app_list = response.context_data["available_apps"]
      context_key = "available_apps"
    else:  # nothing to reorder, return response
      return response

    self.init_config(request, app_list)
    ordered_app_list = self.get_app_list()
    response.context_data[context_key] = ordered_app_list
    return response
