import markdown
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from markdown.inlinepatterns import ImagePattern, IMAGE_LINK_RE

media_url_prefix = settings.MEDIA_URL

register = template.Library()


class AddImagePrefix(ImagePattern):
    def __init__(self, slug=None, *args, **kwargs):
        self.slug = slug
        super(AddImagePrefix, self).__init__(*args, **kwargs)

    def handleMatch(self, m):
        node = ImagePattern.handleMatch(self, m)
        # check 'src' to ensure it is local
        src = node.attrib.get('src')
        node.attrib['src'] = media_url_prefix + self.slug + '/' + src
        return node


mk = markdown.Markdown(extensions=['markdown.extensions.fenced_code',
                                   'markdown.extensions.codehilite'],
                       safe_mode=True,
                       enable_attributes=False)


@register.filter
def markme(value, obj):
    mk.inlinePatterns['image_link'] = AddImagePrefix(pattern=IMAGE_LINK_RE, slug=obj.slug, markdown_instance=mk)
    content = mark_safe(mk.convert(value))

    return content
