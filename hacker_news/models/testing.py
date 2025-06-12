from django.db import models


class Testing(models.Model):
  by = models.CharField(max_length=255)
  descendants = models.IntegerField()
  id = models.IntegerField(primary_key=True)
  kids = models.JSONField()
  score = models.IntegerField()
  time = models.IntegerField()
  title = models.CharField(max_length=255)

  def __str__(self):
    return f"Testing {self.id}"
