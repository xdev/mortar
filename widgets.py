import os

from PIL import Image

from django.contrib.admin.widgets import AdminFileWidget as AdminFileWidgetBase
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import get_model
from django import forms
from django.utils import simplejson

from easy_thumbnails.files import Thumbnailer

def thumbnail(imagefile):
    t = Thumbnailer(imagefile)
    f = t.get_thumbnail({'size':(200,200)})
    return '<img src="%s" alt="An Image">' % f._get_url()

class AdminFileWidget(AdminFileWidgetBase):
    def __init__(self, *args, **kwargs):
        try:
            self.allow_remove = kwargs.pop('allow_remove')
        except:
            self.allow_remove = True
        super(AdminFileWidget, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s/%s' % (settings.MEDIA_URL, file_name)
            if self.allow_remove:
                output.append("""
                <input type="checkbox" style="margin: 0;" name="remove_%s" id="id_remove_%s"/><label style="display: inline; width: 30px;" for="id_remove_%s">Delete?</label><br>
                """ % (name, name, name))
            output.append("""
            %s
            <a target="_blank" href="%s">%s</a><br>%s<br />
            <br />
            """ % (_('Currently:'), file_path, file_name, _('Change:')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
    

class AdminImageWidget(AdminFileWidgetBase):
    def __init__(self, *args, **kwargs):
        try:
            self.allow_remove = kwargs.pop('allow_remove')
        except:
            self.allow_remove = True
        super(AdminImageWidget, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s/%s' % (settings.MEDIA_URL, file_name)
            try:
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                if self.allow_remove:
                    output.append("""
                    <input type="checkbox" style="margin: 0;" name="remove_%s" id="id_remove_%s"/><label style="display: inline; width: 30px;" for="id_remove_%s">Delete?</label>
                    """ % (name, name, name))
                output.append("""
                <a target="_blank" href="%s">%s</a><br>%s
                <a target="_blank" href="%s">%s</a><br>%s<br />
                <br />
                """ % \
                (file_path, thumbnail(file(file_name)), _('Currently:'), file_path,
                file_name, _('Change:')))
            except IOError:
                output.append('%s <a target="_blank" href="%s">%s</a> <br>%s ' % \
                (_('Currently:'), file_path, file_name, _('Change:')))
        output.append(super(AdminFileWidgetBase, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
    

