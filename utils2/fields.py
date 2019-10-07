# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.db import models
import  json
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.forms import forms

from decimal import Decimal
import datetime

from forms import JSONFormField


def default(o):
    if hasattr(o, 'to_json'):
        return o.to_json()
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, datetime.datetime):
        return o.strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, datetime.time):
        return o.strftime("%H:%M:%S")

    raise TypeError(repr(o) + " is not JSON serializable")


class JSONField(models.TextField):
    """
    A field that will ensure the data entered into it is valid JSON.
    """
    __metaclass__ = models.SubfieldBase
    default_error_messages = {
        'invalid': _(u"'%s' is not a valid JSON string.")
    }
    description = "JSON object"

    def __init__(self, *args, **kwargs):
        if not kwargs.get('null', False):
            kwargs['default'] = kwargs.get('default', {})
        super(JSONField, self).__init__(*args, **kwargs)
        if 'default' in kwargs:
            if callable(self.default):
                self.validate(self.default(), None)
            else:
                self.validate(self.default, None)

    def formfield(self, **kwargs):
        return super(JSONField, self).formfield(form_class=JSONFormField, **kwargs)

    def validate(self, value, model_instance):
        if not self.null and value is None:
            raise ValidationError(self.error_messages['null'])
        try:
            self.get_prep_value(value)
        except:
            raise ValidationError(self.error_messages['invalid'] % value)

    def get_default(self):
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return super(JSONField, self).get_default()

    def to_python(self, value):
        if isinstance(value, basestring):
            if value == "":
                if self.null:
                    return None
                if self.blank:
                    return ""
            try:
                value = json.loads(value)
            except ValueError:
                msg = self.error_messages['invalid'] % str(value)
                raise ValidationError(msg)
        # TODO: Look for date/time/datetime objects within the structure?
        return value

    def get_db_prep_value(self, value, connection=None, prepared=None):
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if value is None:
            if not self.null and self.blank:
                return ""
            return None
        return json.dumps(value, default=default)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ["exact", "iexact"]:
            return self.to_python(self.get_prep_value(value))
        if lookup_type == "in":
            return [self.to_python(self.get_prep_value(v)) for v in value]
        if lookup_type == "isnull":
            return value
        if lookup_type in ["contains", "icontains"]:
            if isinstance(value, (list, tuple)):
                raise TypeError("Lookup type %r not supported with argument of %s" % (
                    lookup_type, type(value).__name__
                ))
                # Need a way co combine the values with '%', but don't escape that.
                return self.get_prep_value(value)[1:-1].replace(', ', r'%')
            if isinstance(value, dict):
                return self.get_prep_value(value)[1:-1]
            return self.to_python(self.get_prep_value(value))
        raise TypeError('Lookup type %r not supported' % lookup_type)

    def value_to_string(self, obj):
        return self._get_val_from_obj(obj)


class ContentTypeRestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, content_types=None, max_upload_size=None, **kwargs):
        self.content_types = content_types
        self.max_upload_size = max_upload_size
        super(ContentTypeRestrictedFileField, self).__init__(**kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_(u'Допустимый размер файла %s. Текущий размер %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_(u'Неверный формат.'))
        except AttributeError:
            pass

        return data


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^utils\.fields\.JSONField'])
    add_introspection_rules([], ['^utils\.fields\.ContentTypeRestrictedFileField'])
    add_introspection_rules([], ['^utils2\.fields\.JSONField'])
    add_introspection_rules([], ['^utils2\.fields\.ContentTypeRestrictedFileField'])
except ImportError:
    pass
