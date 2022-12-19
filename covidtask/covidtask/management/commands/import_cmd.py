from django.core.management.base import BaseCommand, CommandError
from covidtask.models import Country,CountriesHistory
from django.db.models import Count
import requests
class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            countries = Country.objects.annotate(subscriptions_count=Count('subscription')).filter(subscriptions_count__gt =0 ).all()

            for country in countries:
                response = requests.get('https://api.covid19api.com/country/'+country.name).json()
                death = 0
                confirmed = 0
                recoverd = 0
                if len(response) > 1:
                    for record in response:
                        death+=record['Deaths']
                        confirmed+=record['Confirmed']
                        recoverd+=record['Recovered']
                    CountriesHistory.objects.create(country_id=country,death=country.death,confirmed=country.confirmed,recoverd=country.recoverd)
                    Country.objects.filter(name=country.name).update(death=death,confirmed=confirmed,recoverd=recoverd)


        except Exception as e:
            raise CommandError(e)