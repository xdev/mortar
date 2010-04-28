import os

from PIL import Image

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import get_model
from django import forms
from django.utils import simplejson

from sorl.thumbnail.base import Thumbnail

from topics.models import Topic

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

class AdminImageWidget(AdminFileWidget):
  """
  A FileField widget that displays an image instead of a file path
  if the current file is an image.
  """

  def render(self, name, value, attrs=None):
    output = []
    file_name = str(value)
    if file_name:
      file_path = '%s/%s' % (settings.MEDIA_URL, file_name)
      try:
        Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
        output.append("""
        <a target="_blank" href="%s">%s</a><br>%s
        <a target="_blank" href="%s">%s</a><br>%s """ % \
            (file_path, thumbnail(file_name), _('Currently:'), file_path,
              file_name, _('Change:')))
      except IOError:
        output.append('%s <a target="_blank" href="%s">%s</a> <br>%s ' % \
            (_('Currently:'), file_path, file_name, _('Change:')))

    output.append(super(AdminFileWidget, self).render(name, value, attrs))
    return mark_safe(u''.join(output))

class AutoCompleteTagInput(forms.TextInput):
    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',)
        }
        js = (
            'js/jquery.js',
            'js/jquery.bgiframe.min.js',
            'js/jquery.ajaxQueue.js',
            'js/jquery.autocomplete.js'
        )

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        topics = Topic.objects.all()
        topic_list = simplejson.dumps([topic.name for topic in topics],
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            jQuery("#id_%s").autocomplete(%s, {
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
            });
            </script>''' % (name, topic_list))
