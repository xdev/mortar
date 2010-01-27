# Authors: Marinho Brandao <marinho at gmail.com>
#          Guilherme M. Gondim (semente) <semente at taurinus.org>
# File: <your project>/admin/filterspecs.py

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class AlphabeticFilterSpec(ChoicesFilterSpec):
    """
    Adds filtering by first char (alphabetic style) of values in the admin
    filter sidebar. Set the alphabetic filter in the model field attribute
    'alphabetic_filter'.

    my_model_field.alphabetic_filter = True
    """

    def __init__(self, f, request, params, model, model_admin):
        super(AlphabeticFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin)
        self.lookup_kwarg = '%s__istartswith' % f.name
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        values_list = model.objects.values_list(f.name, flat=True)
        # getting the first char of values
        self.lookup_choices = list(set(val[0] for val in values_list if val))
        self.lookup_choices.sort()

    def choices(self, cl):
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for val in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                    'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                    'display': val.upper()}
    def title(self):
      return _('%(field_name)s starting with:') % \
            {'field_name': self.field.verbose_name}

# registering the filter
FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'alphabetic_filter', False),
                                   AlphabeticFilterSpec))

