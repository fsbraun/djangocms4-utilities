from django.core.management.base import BaseCommand, CommandError
from djangocms4_utilities.utilities import plugintree


class Command(BaseCommand):
    args = '<none>'
    help = 'Runs fix_tree for every draft placeholder'

    def handle(self, *args, **options):
        for placeholder in plugintree.Placeholder.objects.all():
            self.stdout.write(f"Fixing {placeholder.slot} (id={placeholder.id})")
            languages = placeholder.cmsplugin_set.values_list('language', flat=True).distinct()
            for language in languages:
                plugintree.fix_tree(placeholder, language)
