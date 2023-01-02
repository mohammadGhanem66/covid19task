from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Country, CountryDailyCases
from datetime import datetime


class TestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='admin@admin.com', password='helloworld')
        self.country_palestine = Country.objects.create(name="palestine")
        self.country_jordan = Country.objects.create(name="jordan")
        date = datetime.fromisoformat("2020-01-22T00:00:00Z"[:-1] + '+00:00')
        CountryDailyCases.objects.create(country_id=self.country_palestine, death=10,
                                         confirmed=20, recoverd=10,
                                         death_agg=10, confirmed_agg=20,
                                         recoverd_agg=10, date=date)
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.authentication()

    def authentication(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = "Bearer " + self.token

    def test_subscribe(self):
        payload = {
            "country": "aue"
        }
        response = self.client.post('/subscribe/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_death_percentage(self):
        country = self.country_palestine.name
        response = self.client.get(f'/country/{country}/death-percentage')
        responseJson = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(responseJson["percentage"], 0.5)

    def test_top_countries(self):
        payload = {
            'status': 'death',
            'limit': 1
        }
        response = self.client.get('/country/top/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = {
            'status': 'confirmed',
            'limit': 3
        }
        response = self.client.get('/country/top/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_death_percentage_unauth(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = ""
        country = self.country_palestine.name
        response = self.client.get(f'/country/{country}/death-percentage')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_top_countries_empty_payload(self):
        payload = {}
        response = self.client.get('/country/top/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe_empty_payload(self):
        payload = {}
        response = self.client.post('/subscribe/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
