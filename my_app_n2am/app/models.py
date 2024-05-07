from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(default=None)

    def __str__(self):
        return self.name
    