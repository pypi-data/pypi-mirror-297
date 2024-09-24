from django.db import models
from django.utils import timezone


class LRNDKey(models.Model):
    key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    def __str__(self):
        return f"LRND Key {self.id}"