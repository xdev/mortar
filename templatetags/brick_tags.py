import re

from django import template
from django.template import Node

register = template.Library()

@register.tag
def active(parser, token):
    import re
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])

class NavSelectedNode(template.Node):
    def __init__(self, patterns):
        self.patterns = patterns
    def render(self, context):
        path = context['request'].path
        for p in self.patterns:
            pValue = template.Variable(p).resolve(context)
            if path == pValue:
                return "current"
        return ""

class SplitListNode(Node):
    def __init__(self, old_list, cols, new_list):
        self.old_list, self.cols, self.new_list = old_list, cols, new_list

    def split_seq(self, old_list, cols=2):
        start = 0
        for i in xrange(cols):
            stop = start + len(old_list[i::cols])
            yield old_list[start:stop]
            start = stop

    def render(self, context):
        context[self.new_list] = self.split_seq(context[self.old_list],
            int(self.cols))
        return ''

@register.tag
def list_to_columns(parser, token):
    """ Parse template tag: {% list_to_columns list as new_list 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "list_to_columns list as new_list 2"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "Second argument to the list_to_columns tag must be 'as'"
    return SplitListNode(bits[1], bits[4], bits[3])

