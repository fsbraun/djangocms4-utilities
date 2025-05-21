from django.core.management.base import BaseCommand, CommandError
from djangocms4_utilities.utilities import plugintree


class Command(BaseCommand):
    args = '<none>'
    help = 'Runs fix_tree for every draft placeholder'
    def add_arguments(self, parser):
        parser.add_argument(
            'placeholder_ids',
            nargs='*',
            type=int,
            help='Optional list of placeholder IDs to fix. If omitted, all placeholders will be fixed.',
        )

    def handle(self, *args, **options):
        placeholder_ids = options['placeholder_ids']

        if placeholder_ids:
            placeholders = plugintree.Placeholder.objects.filter(id__in=placeholder_ids)
            if not placeholders.exists():
                raise CommandError(f"No placeholders found with IDs: {placeholder_ids}")
        else:
            placeholders = plugintree.Placeholder.objects.all()

        for placeholder in placeholders:
            self.stdout.write(f"Fixing {placeholder.slot} (id={placeholder.id})")
            languages = placeholder.cmsplugin_set.values_list('language', flat=True).distinct()
            for language in languages:
                plugintree.fix_tree(placeholder, language)
