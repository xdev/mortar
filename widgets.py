import os

from PIL import Image

from django.contrib.admin.widgets import AdminFileWidget as AdminFileWidgetBase
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import get_model
from django import forms
from django.utils import simplejson

from sorl.thumbnail.base import Thumbnail

try:
  from sorl.thumbnail.main import DjangoThumbnail
  def thumbnail(image_path):
    t = DjangoThumbnail(relative_source=image_path,
        requested_size=(200,200))
    return u'<img src="%s" alt="%s" class="sorl">' % (t.absolute_url,
        image_path)
except ImportError:
  def thumbnail(image_path):
    absolute_url = os.path.join(settings.MEDIA_URL, image_path)
    return u'<img src="%s" alt="%s">' % (t.absolute_url, image_path)

class AdminFileWidget(AdminFileWidgetBase):
  """
  A FileField widget that displays an image instead of a file path
  if the current file is an image.
  """
  
  def __init__(self, attrs=None):
      super(AdminFileWidget, self).__init__(attrs)
  
  def render(self, name, value, attrs=None):
    output = []
    file_name = str(value)
    if file_name:
      file_path = '%s/%s' % (settings.MEDIA_URL, file_name)
      
      output.append("""
      <input type="checkbox" style="margin: 0;" name="remove_%s" id="id_remove_%s"/><label style="display: inline; width: 30px;" for="id_remove">Delete?</label>
      <br>%s
      <a target="_blank" href="%s">%s</a><br>%s<br />
      <br />
      """ % (name, name, _('Currently:'), file_path, file_name, _('Change:')))
      
    
    output.append(super(AdminFileWidget, self).render(name, value, attrs))
    return mark_safe(u''.join(output))


class AdminImageWidget(AdminFileWidgetBase):
  """
  A FileField widget that displays an image instead of a file path
  if the current file is an image.
  """
  
  def __init__(self, attrs=None):
      super(AdminImageWidget, self).__init__(attrs)
  
  def render(self, name, value, attrs=None):
    output = []
    file_name = str(value)
    if file_name:
      file_path = '%s/%s' % (settings.MEDIA_URL, file_name)
      try:
        Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
        output.append("""
        <input type="checkbox" style="margin: 0;" name="remove_%s" id="id_remove_%s"/><label style="display: inline; width: 30px;" for="id_remove">Delete?</label>
        <a target="_blank" href="%s">%s</a><br>%s
        <a target="_blank" href="%s">%s</a><br>%s<br />
        <br />
        """ % \
            (name, name, file_path, thumbnail(file_name), _('Currently:'), file_path,
              file_name, _('Change:')))
      except IOError:
        output.append('%s <a target="_blank" href="%s">%s</a> <br>%s ' % \
            (_('Currently:'), file_path, file_name, _('Change:')))
    
    output.append(super(AdminFileWidgetBase, self).render(name, value, attrs))
    return mark_safe(u''.join(output))

