from django.core.management.base import BaseCommand
from show_result.models import house

# collect data from ssa website and write into sqlite database

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        house.objects.all().delete()