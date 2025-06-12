from django.db import models


class User(models.Model):
  id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=255)
  karma = models.IntegerField()
  created_on = models.DateTimeField()
  updated_on = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "user"
    verbose_name_plural = "Users"
  
  def __str__(self):
    return f"{self.id} - {self.username}"
