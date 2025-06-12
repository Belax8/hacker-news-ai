from django.db import models

from .story import Story


class Article(models.Model):
  id = models.AutoField(primary_key=True)
  story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='articles')
  text = models.TextField(null=True, blank=True)
  created_on = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "article"
    verbose_name_plural = "Articles"
  
  def __str__(self):
    return f"{self.id} - {self.text[:20]}..."
