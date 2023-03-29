from django.db import models

class Todo(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    isComplete = models.BooleanField(default=False)