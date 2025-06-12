from django.db import models

from .user import User


class Story(models.Model):
  id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=255, null=False, blank=False)
  text = models.TextField(null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  score = models.IntegerField(null=True, blank=True)
  url = models.URLField(null=True, blank=True)
  is_deleted = models.BooleanField(default=False)
  created_on = models.DateTimeField()
  updated_on = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "story"
    verbose_name_plural = "Stories"
  
  def __str__(self):
    return f"{self.id} - {self.title[:20]}..."
