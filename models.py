import datetime

from django.db import models
from django.contrib.auth.models import User

"""
Proxy models for user accounts to clean up display in Django admin
"""
class Customer(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'User account'
        verbose_name_plural = 'User accounts'

class Staff(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Staff account'
        verbose_name_plural = 'Staff accounts'

class AutoDateTimeField(models.DateTimeField):
  """ Field to save current date and time """
  def pre_save(self, model_instance, add):
    return datetime.datetime.now()

class CommonAbstractModel(models.Model):
  """
  Common ABC for most models.
  Provides created/updated_at, and active/inactive status.
  """
  created_at = models.DateTimeField(
    default=datetime.datetime.now(), editable=False)
  updated_at = AutoDateTimeField(editable=False)
  active = models.BooleanField(default=True, verbose_name="published")
  
  class Meta:
    get_latest_by = 'updated_at'
    ordering = ('-updated_at', '-created_at')
    abstract = True
