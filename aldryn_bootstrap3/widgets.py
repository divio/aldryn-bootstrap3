# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import django.forms.widgets
from django.template.loader import render_to_string

from .conf import settings


class SelectFieldCompatMixin(object):
    """
    This class is only needed for Django < 1.11 compatibility
    """

    @property
    def renderer(self):
        class Renderer(django.forms.widgets.RadioFieldRenderer):
            template_name = self.template_name

            def render(self):
                return render_to_string(self.template_name, {'selects': self})
        return Renderer


class Context(SelectFieldCompatMixin, django.forms.widgets.RadioSelect):
    template_name = 'admin/aldryn_bootstrap3/widgets/context.html'


class Size(SelectFieldCompatMixin, django.forms.widgets.RadioSelect):
    template_name = 'admin/aldryn_bootstrap3/widgets/size.html'


class LinkOrButton(SelectFieldCompatMixin, django.forms.widgets.RadioSelect):
    template_name = 'admin/aldryn_bootstrap3/widgets/link_or_button.html'


class Icon(django.forms.widgets.TextInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super(Icon, self).render(name, value, attrs=attrs, **kwargs)
        if value is None:
            value = ''
        iconset = value.split('-')[0] if value and '-' in value else ''
        iconset_prefexes = [s[1] for s in settings.ALDRYN_BOOTSTRAP3_ICONSETS]
        if len(settings.ALDRYN_BOOTSTRAP3_ICONSETS) and iconset not in iconset_prefexes:
            # invalid iconset! maybe because the iconset was removed from
            # the project. set it to the first in the list.
            iconset = settings.ALDRYN_BOOTSTRAP3_ICONSETS[0][1]
        rendered = render_to_string(
            'admin/aldryn_bootstrap3/widgets/icon.html',
            {
                'input_html': input_html,
                'value': value,
                'name': name,
                'iconset': iconset,
                'is_required': self.is_required,
                'iconsets': settings.ALDRYN_BOOTSTRAP3_ICONSETS,
            },
        )
        return rendered


class MiniTextarea(django.forms.widgets.Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['cols'] = '120'
        attrs['rows'] = '1'
        super(MiniTextarea, self).__init__(attrs)


class Responsive(django.forms.widgets.Textarea):
    def render(self, name, value, attrs=None):
        widget_html = super(Responsive, self).render(name=name, value=value, attrs=attrs)

        rendered = render_to_string(
            'admin/aldryn_bootstrap3/widgets/responsive.html',
            {
                'widget_html': widget_html,
                'widget': self,
                'value': value,
                'name': name,
                'id': attrs.get('id', None),
                'attrs': attrs,
            },
        )
        return rendered


class ResponsivePrint(django.forms.widgets.Textarea):
    def render(self, name, value, attrs=None):
        widget_html = super(ResponsivePrint, self).render(
            name=name, value=value, attrs=attrs)

        rendered = render_to_string(
            'admin/aldryn_bootstrap3/widgets/responsive_print.html',
            {
                'widget_html': widget_html,
                'widget': self,
                'value': value,
                'name': name,
                'id': attrs.get('id', None),
                'attrs': attrs,
            },
        )
        return rendered
