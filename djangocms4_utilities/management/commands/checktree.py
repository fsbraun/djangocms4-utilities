from django.core.management.base import BaseCommand, CommandError
from djangocms4_utilities.utilities import plugintree


class Command(BaseCommand):
    args = '<none>'
    help = 'Runs check_tree for every draft placeholder and prints inconsistencies ' \
           'to the console'

    def handle(self, *args, **options):
        plugintree.check_placeholders(plugintree.Pladceholder.objects.all())
