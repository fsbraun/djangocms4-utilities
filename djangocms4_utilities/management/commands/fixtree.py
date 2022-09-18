from django.core.management.base import BaseCommand, CommandError
from djangocms4_utilities.utilities import plugintree


class Command(BaseCommand):
    args = '<none>'
    help = 'Runs a fix tree for every draft placeholder'

    def handle(self, *args, **options):
        for placeholder in plugintree.get_draft_placeholders():
            self.stdout.write(f"Fixing placeholder {placeholder.slot} (id={placeholder.id})")
            plugintree.fix_tree(placeholder)
