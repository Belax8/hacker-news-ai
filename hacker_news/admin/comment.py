from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
  list_display = ["id", "story", "user", "text", "created_on", "updated_on", "is_deleted"]
  list_filter = ["is_deleted"]
  search_fields = ["text"]