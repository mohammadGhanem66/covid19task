from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscription = models.ManyToManyField(User, related_name="subscriptions", db_table="Subscription",
                                          verbose_name="subscriptions", blank=True, null=True)

    def __str__(self):
        return self.name


class CountryDailyCases(models.Model):
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_daily_cases")
    confirmed = models.IntegerField(blank=True, null=True)
    death = models.IntegerField(blank=True, null=True)
    recoverd = models.IntegerField(blank=True, null=True)
    confirmed_agg = models.IntegerField(blank=True, null=True)
    death_agg = models.IntegerField(blank=True, null=True)
    recoverd_agg = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        country = self.country_id.name
        created_at = self.created_at
        return f"{country} {created_at}"
