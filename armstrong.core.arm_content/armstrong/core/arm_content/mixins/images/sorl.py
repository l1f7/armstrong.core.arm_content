from .base import BaseThumbnailMixin
from ...images.sorl import get_preset_thumbnail

class SorlThumbnailMixin(BaseThumbnailMixin):
    visual_field_name = 'image'

    def render_visual(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        # TODO: Use a template for this.
        url, dimensions = self.get_visual_thumbnail_url(preset_label, presets, defaults, *args, **kwargs)
        try:
            width, height = dimensions.split('x')
        except ValueError: # height doesn't exist
            width = dimensions
            height = False
        return '<img src="%s" />' % (url)

    def get_visual_thumbnail_url(self, preset_label, presets=None, defaults=None, *args, **kwargs):
        image_file = getattr(self, self.visual_field_name)
        thumbnail_file, dimensions = get_preset_thumbnail(image_file, preset_label, presets, defaults)
        return (thumbnail_file.url, dimensions)
