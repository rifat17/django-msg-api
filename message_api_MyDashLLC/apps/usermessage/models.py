from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import (
    get_user_model,
)


User = get_user_model()



class MessageReqModel(models.Model):
    message = models.CharField(max_length=1000, blank=True)

class MessagDBModel(models.Model):
    message = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"msg : {self.message}, created_at : {self.created_at.ctime()}"
