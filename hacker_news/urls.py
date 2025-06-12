"""
URL configuration for hacker_news project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from hacker_news.admin import admin_site
from hacker_news.views import index, ping, story, summarize_story

urlpatterns = [
  path('', index.index, name='index'),
  path('ping', ping.ping, name='ping'),
  path('admin', admin_site.urls),
  path('story/<int:story_id>', story.story, name='story'),
  path('api/summarize-story/<int:story_id>', summarize_story.summarize_story, name='summarize_story'),
]
