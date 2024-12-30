from django.db import models

# Create your models here.

class Visitor(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField()

    def __str__(self):
        return self.name if self.name else "Unnamed Visitor"

