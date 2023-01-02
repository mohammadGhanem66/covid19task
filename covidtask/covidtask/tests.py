from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Country

class TestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='admin@admin.com', password='helloworld')
        self.country_palestine = Country.objects.create(name="Palestine")
        self.country_jordan = Country.objects.create(name="Jordan")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.authentication()

    def authentication(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = "Bearer "+ self.token

    def test_subscribe(self):
        payload = {
            "countries": [self.country_palestine.name,self.country_jordan.name]
        }
        response = self.client.post('/subscribe/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        responseJson = response.json()
        self.assertEqual(responseJson["message"], "sucess")

    def test_death_percentage(self):
        payload = {
            'country':self.country_palestine.name
        }
        response = self.client.get('/country/death-percentage/',payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_countries(self):
        payload = {
            'status':'death',
            'limit':3
        }
        response = self.client.get('/country/top/',payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_countries(self):
        response = self.client.get('/country/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_countries_unauth(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = ""
        response = self.client.get('/country/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_death_percentage_empty_payload(self):
        payload = {}
        response = self.client.get('/country/death-percentage/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_countries_empty_payload(self):
        payload = {}
        response = self.client.get('/country/top/',payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe_empty_payload(self):
        payload = {}
        response = self.client.post('/subscribe/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

