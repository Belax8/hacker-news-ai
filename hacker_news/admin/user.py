from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
  list_display = ["id", "username", "karma", "created_on", "updated_on"]
  search_fields = ["username"]