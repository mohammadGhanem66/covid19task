from django.core.management.base import BaseCommand, CommandError
from covidtask.models import Country
import requests
class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            response = requests.get('https://api.covid19api.com/countries').json()
            for record in response:
                Country.objects.create(name=record['Slug'])

        except Exception as e:
            raise CommandError(e)