from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=255)
    confirmed = models.IntegerField(blank=True, null = True)
    death = models.IntegerField(blank=True, null = True)
    recoverd = models.IntegerField(blank=True, null = True)
    updated_at = models.DateTimeField(auto_now=True)
    subscription = models.ManyToManyField(User,related_name ="subscriptions",db_table="Subscription",verbose_name="subscriptions",blank=True,null = True)
    def __str__(self):
        return self.name

class CountriesHistory(models.Model):
    country_id = models.ForeignKey(Country,on_delete=models.CASCADE)
    confirmed = models.IntegerField(blank=True, null = True)
    death = models.IntegerField(blank=True, null = True)
    recoverd = models.IntegerField(blank=True, null = True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.country_id.name+" "+str(self.created_at)