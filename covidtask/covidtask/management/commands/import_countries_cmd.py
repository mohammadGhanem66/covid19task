from django.core.management.base import BaseCommand, CommandError
from covidtask.models import Country
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            response = requests.get('https://api.covid19api.com/countries')
            if response.status_code > 299:
                print("The API is not available")
                exit()
            response = response.json()
            for record in response:
                Country.objects.create(name=record['Slug'])

        except Exception as e:
            raise CommandError(e)
