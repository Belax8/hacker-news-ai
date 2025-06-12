from django.db import models

from .story import Story
from .user import User


class Comment(models.Model):
  id = models.IntegerField(primary_key=True)
  story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
  parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  text = models.TextField(null=True, blank=True)
  is_deleted = models.BooleanField(default=False)
  created_on = models.DateTimeField()
  updated_on = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "comment"
    verbose_name_plural = "Comments"
  
  def __str__(self):
    if self.text:
      return f"{self.id} - {self.text[:50]}..."
    else:
      return f"{self.id} - "
