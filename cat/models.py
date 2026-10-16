from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=1)
    fullness = models.PositiveIntegerField(default=40)
    happiness = models.PositiveIntegerField(default=40)
    is_sleeping = models.BooleanField(default=False)

    def __str__(self):
        return self.name
