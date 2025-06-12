from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
  list_display = ["id", "story", "created_on"]
  search_fields = ["text"]