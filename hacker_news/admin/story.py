from django.contrib import admin
from django.utils.html import format_html


class StoryAdmin(admin.ModelAdmin):
  list_display = ["id", "link", "title", "user", "score", "url", "is_deleted"]
  search_fields = ["title", "text"]
  list_filter = ["is_deleted"]

  def link(self, obj):
    url = f'/story/{obj.id}'
    return format_html('<a href="{}">link</a>', url)