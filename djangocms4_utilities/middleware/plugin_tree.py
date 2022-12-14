import sys

from django.conf import settings
from django.core.management.base import OutputWrapper, color_style

from cms.models.placeholdermodel import Placeholder

from ..utilities.plugintree import check_placeholders


stdout = OutputWrapper(sys.stdout)
stdout.style = color_style()

def watch(get_response):
    def middleware(request):
        response = get_response(request)  # Execute view
        if getattr(settings, "WATCH_PLACEHOLDER", None) is not None:
            placeholders = settings.WATCH_PLACEHOLDER
            placeholders = [placeholders] if isinstance(placeholders, int) else placeholders
            placeholders = Placeholder.objects.filter(id__in=placeholders)
            if not placeholders:
                stdout.write(f"Placeholders {settings.WATCH_PLACEHOLDER} not found.", stdout.style.WARNING)
            else:
                check_placeholders(placeholders)
        return response

    return middleware
