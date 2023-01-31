from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
import re


register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(
        value,
        extensions=['extra']
    )

@register.filter()
@stringfilter
def script_escape(value: str):

    value = re.sub("\<\s*script.*?\s*?\>", "&lt;script&gt;", value)
    value = re.sub("\<\s*\/\s*script.*?\s*?\>", "&lt;/script&gt;", value)
    # value = value.replace('<script>', "&lt;script&gt;")
    # value = value.replace('</script>', "&lt;/script&gt;")
    return value
