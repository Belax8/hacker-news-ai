from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpRequest

from hacker_news.admin.comment import CommentAdmin
from hacker_news.admin.user import UserAdmin
from hacker_news.admin.story import StoryAdmin
from hacker_news.admin.article import ArticleAdmin
from hacker_news.models.article import Article
from hacker_news.models.comment import Comment
from hacker_news.models.story import Story
from hacker_news.models.user import User


class HackerNewsSite(admin.AdminSite):
  site_header = "Hacker News AI Admin"
  site_title = "Hacker News AI"
  index_title = "Admin"

  def each_context(self, request: HttpRequest) -> dict:
    context = super().each_context(request)
    context.update(
      {
        "site_header": self.site_header,
        "site_title": self.site_title,
        "index_title": self.index_title,
      }
    )
    return context


admin_site = HackerNewsSite(name="admin")

# Hacker News
admin_site.register(User, UserAdmin)
admin_site.register(Story, StoryAdmin)
admin_site.register(Article, ArticleAdmin)
admin_site.register(Comment, CommentAdmin)

# Auth
admin_site.register(DjangoUser, DjangoUserAdmin)
admin_site.register(DjangoGroup, DjangoGroupAdmin)
