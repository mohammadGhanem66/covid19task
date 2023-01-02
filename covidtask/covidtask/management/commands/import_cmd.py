from django.core.management.base import BaseCommand, CommandError
from covidtask.models import Country, CountryDailyCases
from django.db.models import Count
import requests
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            countries = Country.objects.annotate(subscriptions_count=Count('subscription')).filter(
                subscriptions_count__gt=0).all()

            for country in countries:
                response = requests.get('https://api.covid19api.com/country/' + country.name)
                if response.status_code > 299:
                    print("The API is not available")
                    continue

                response = response.json()
                if len(response) > 1:
                    try:
                        country_history = country.country_daily_cases.latest('created_at')
                    except CountryDailyCases.DoesNotExist:
                        country_history = None

                    if not country_history:
                        death_agg = 0
                        confirmed_agg = 0
                        recoverd_agg = 0
                    else:
                        death_agg = country_history.death_agg
                        confirmed_agg = country_history.confirmed_agg
                        recoverd_agg = country_history.recoverd_agg
                    
                    for record in self.filter_response(response, country_history):
                        death_agg += record['Deaths']
                        confirmed_agg += record['Confirmed']
                        recoverd_agg += record['Recovered']
                        date = datetime.fromisoformat(record['Date'][:-1] + '+00:00')
                        CountryDailyCases.objects.create(country_id=country, death=record['Deaths'],
                                                         confirmed=record['Confirmed'], recoverd=record['Recovered'],
                                                         death_agg=death_agg, confirmed_agg=confirmed_agg,
                                                         recoverd_agg=recoverd_agg, date=date)


        except Exception as e:
            raise CommandError(e)

    def filter_response(self, response, country_history):
        if not country_history:
            return response
        return filter(lambda record: datetime.fromisoformat(
            record['Date'][:-1] + '+00:00').date() > country_history.date.date(), response)
