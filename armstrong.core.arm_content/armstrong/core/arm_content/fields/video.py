from django.db import models
from django.core.exceptions import ValidationError
from ..video.backends import get_backend


def validate_query_string(value):
    if value.find('v=') == -1:
        raise ValidationError(u'%s is not a properly formatted YouTube URL' % value)



class EmbeddedVideo(object):
    def __init__(self, url=None, backend=None):
        if not backend:
            backend = get_backend()
        self.backend = backend
        self.raw_url = url
        self.id = None
        if url:
            self.backend.prepare(self)

    @property
    def type(self):
        return self.backend.type

    def embed(self, **kwargs):
        return self.backend.embed(self, **kwargs)

    def __len__(self):
        return len(self.raw_url)

    def __unicode__(self):
        return self.raw_url



class EmbeddedVideoField(models.URLField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(EmbeddedVideoField, self).__init__(self, *args, **kwargs)

    def get_prep_value(self, value):
        return value.raw_url

    def to_python(self, value):
        if isinstance(value, EmbeddedVideo):
            return value

        return EmbeddedVideo(value)

    def formfield(self, **kwargs):
        defaults = {
            "label": "Embedded Video URL",
            'validators': [validate_query_string]
        }
        defaults.update(**kwargs)
        return super(EmbeddedVideoField, self).formfield(**defaults)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "%s.%s" % (self.__class__.__module__,
                self.__class__.__name__)
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
