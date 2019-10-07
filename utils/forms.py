#-*- coding:utf-8 -*-
import random
from urlparse import urljoin

from django import forms
from django.forms.utils import flatatt
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.conf import settings
from django.forms import Media, Textarea
import json

from widgets import JSONWidget


class JSONFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = JSONWidget
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            return value
        if isinstance(value, basestring):
            try:
                return json.loads(value)
            except Exception, exc:
                raise forms.ValidationError(u'JSON decode error: %s' % (unicode(exc),))
        else:
            return value


class GoogleMapWidget(forms.TextInput):
    input_type = u'hidden'

    def __init__(self, attrs=None):
        default_attrs = {'map_width': '400', 'map_height': '300', 'map_zoom': 8, 'map_prefix': random.randint(0, 100)}
        if attrs:
            default_attrs.update(attrs)
        super(GoogleMapWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        # required u'<script type="text/javascript" src="https://maps.google.com/maps/api/js?sensor=true"></script>'
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        initial_marker = ""
        if value != '':
            final_attrs['value'] = force_unicode(self._format_value(value))
            initial_marker = """
                    var clatlng = new google.maps.LatLng%(value)s;
                    marker_%(map_prefix)s = new google.maps.Marker({ position: clatlng, map: map_%(map_prefix)s, draggable:true, animation: google.maps.Animation.DROP});
                    google.maps.event.addListener(marker_%(map_prefix)s, 'dragend', function(event){
                        document.getElementById('id_%(name)s').value = event.latLng;
                    });

                    """ % {'map_prefix':self.attrs['map_prefix'], 'name':name, 'value':value}
        template = u'<div id="map_canvas_%s" style="width:%spx; height:%spx"></div>' % (self.attrs['map_prefix'], self.attrs['map_width'], self.attrs['map_height'])
        template += u'<input%s />' % flatatt(final_attrs)
        template += """
            <script type="text/javascript">
                var marker_%(map_prefix)s;
                function initialize_%(map_prefix)s() {
                    var latlng = new google.maps.LatLng%(map_center)s;
                    var myOptions = {
                        zoom: %(map_zoom)s,
                        center: latlng,
                        mapTypeId: google.maps.MapTypeId.ROADMAP
                    };
                    var map_%(map_prefix)s = new google.maps.Map(document.getElementById("map_canvas_%(map_prefix)s"), myOptions);
                    %(initial_marker)s
                    google.maps.event.addListener(map_%(map_prefix)s, 'click', function(event) {
                        if (!marker_%(map_prefix)s) {
                            marker_%(map_prefix)s = new google.maps.Marker({ position: event.latLng, map: map_%(map_prefix)s, draggable:true, animation: google.maps.Animation.DROP });
                            marker_%(map_prefix)s.setMap(map_%(map_prefix)s);
                            document.getElementById('id_%(name)s').value = event.latLng;
                            google.maps.event.addListener(marker_%(map_prefix)s, 'dragend', function(event){
                                document.getElementById('id_%(name)s').value = event.latLng;
                            });
                        }
                    });
                }
                initialize_%(map_prefix)s();
            </script>
        """ % {'map_prefix':self.attrs['map_prefix'], 'map_zoom':self.attrs['map_zoom'],  \
                'name':name, 'value':value, 'initial_marker':initial_marker, 'map_center':value or '(49.06784540100258, 33.41734690093995)' }
        return mark_safe(template)

class UserWidget(forms.TextInput):
    input_type = u'hidden'
    def __init__(self, attrs=None):
        default_attrs = {'instance': None }
        if attrs:
            default_attrs.update(attrs)
        super(UserWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        template = ''
        if final_attrs['instance']:
            template += u'<a href="%s"><strong>%s</strong></a>' % (reverse('account_page', kwargs={'uid':final_attrs['instance'].user.id}), final_attrs['instance'].user.get_full_name() or final_attrs['instance'].user.username )
        return mark_safe(template)

class ButtonWidget(forms.TextInput):
    input_type = u'hidden'
    def __init__(self, attrs=None):
        default_attrs = {'instance': None , 'value': u'button'}
        if attrs:
            default_attrs.update(attrs)
        super(ButtonWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        template = ''
        if final_attrs['instance']:
            template = u'<a href="%s" class="btn">%s</a>' % (reverse('delete_participant', kwargs={'tid':final_attrs['instance'].team.id, 'pid':final_attrs['instance'].id}), final_attrs['value'] )
        return mark_safe(template)



class Editor(Textarea):
    """
    A widget that renders a <textarea> element as a Redactor rich tech editor.

    This widget has three additional keyword arguments that a typical ``Textarea``
    wiget does not. They are:

    ``redactor_settings`` - a dictionary of named settings and values. See the
    Redactor `API docs <http://redactorjs.com/docs/settings>`_ for available
    settings. If you provide a string instead of a dictionary, it will be used
    as is.

    ``redactor_css`` - a path to a CSS file to include in the editbale content
    region of the widget. Paths used to specify media can be either relative or
    absolute. If a path starts with '/', 'http://' or 'https://', it will be
    interpreted as an absolute path, and left as-is. All other paths will be
    prepended with the value of the ``STATIC_URL`` setting (or ``MEDIA_URL`` if
    static is not defined).

    Example usage::

        >>> Editor(
                redactor_css = 'styles/bodycopy.css',
                redactor_settings={
                    'lang': 'en',
                    'load': True,
                    'path': False,
                    'focus': False,
                }
            )

        >>> Editor(
                redactor_settings="{lang: 'en'}"
            )

    """

    script_tag = '<script type="text/javascript">Redactor.register(%s);</script>'

    def __init__(self, attrs=None, redactor_css=None, redactor_settings=None):
        super(Editor, self).__init__(attrs=attrs)
        default_settings = {
            'lang': 'en',
            'load': True,
            'path': False,
            'focus': False,
            'autoresize': True
        }
        self.redactor_settings = redactor_settings or default_settings
        if redactor_css:
            self.redactor_settings['css'] = self.get_redactor_css_absolute_path(redactor_css)

    def get_redactor_css_absolute_path(self, path):
        if path.startswith(u'http://') or path.startswith(u'https://') or path.startswith(u'/'):
            return path
        else:
            if settings.STATIC_URL is None:
                prefix = settings.MEDIA_URL
            else:
                prefix = settings.STATIC_URL
            return urljoin(prefix, path)

    @property
    def media(self):
        js = (
            'js/redactor.min.js',
            'js/setup.js',
        )
        css = {
            'screen': [
                'css/redactor.css',
            ]
        }
        return Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        html_class_name = attrs.get('class', '')
        redactor_class = html_class_name and " redactor_content" or "redactor_content"
        html_class_name += redactor_class
        attrs['class'] = html_class_name
        html = super(Editor, self).render(name, value, attrs=attrs)
        if isinstance(self.redactor_settings, basestring):
            html += self.script_tag % self.redactor_settings.replace('\n', '')
        else:
            html += self.script_tag % json.dumps(self.redactor_settings)
        return mark_safe(html)


