import datetime

from django.db import models
from django.db import connection
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField
from django_extensions.db.fields import ModificationDateTimeField

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

qn = connection.ops.quote_name

class AutoDateTimeField(models.DateTimeField):
  """ Field to save current date and time """
  def pre_save(self, model_instance, add):
    return datetime.datetime.now()

class CommonAbstractManager(models.Manager):
  def get_active(self):
      return self.get_query_set().filter(active=True)

class CommonAbstractModel(models.Model):
  """
  Common ABC for most models.
  Provides created/updated_at, and active/inactive status.
  """
  created_at = CreationDateTimeField()
  updated_at = ModificationDateTimeField()
  active = models.BooleanField(default=True, verbose_name="published")
  objects = CommonAbstractManager()
  
  class Meta:
    get_latest_by = 'updated_at'
    ordering = ('-updated_at', '-created_at')
    abstract = True
