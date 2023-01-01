from rest_framework.response import Response
from .models import Country, CountryDailyCases
from .serializers import CountrySerializer, SubscribtionSerializer, CountryViewSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import views, status
from django.db.models import Count


class CountryPercentageView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def get(self, request, country, *args, **kwargs):

        country = Country.objects.filter(name=country).first()
        if not country:
            return Response({'message': 'Country not found', 'error': False, 'code': 400},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            country_history = country.country_daily_cases.latest('created_at')
        except CountryDailyCases.DoesNotExist:
            country_history = None

        if country_history:
            death_count = country_history.death_agg
            confirmed_count = country_history.confirmed_agg
            if not confirmed_count:
                return Response({'message': 'Confirmed cant be zero', 'error': False, 'code': 500},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            percentage = death_count / confirmed_count
            responseData = {"death": death_count, "confirmed": confirmed_count, "percentage": percentage}
        else:
            responseData = {"death": 0, "confirmed": 0, "percentage": 0}
        return Response(responseData)


class TopCountryView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def get(self, request, *args, **kwargs):
        country_view_serializer = CountryViewSerializer(data=request.query_params)
        country_view_serializer.is_valid(raise_exception=True)
        data = country_view_serializer.validated_data
        status_agg = data['status'] + "_agg"
        subscribed_countries = Country.objects.annotate(subscriptions_count=Count('subscription')) \
            .filter(subscriptions_count__gt=0).all()
        countries_history = [self.get_latest_country_daily_cases(country) for country in subscribed_countries]
        countries_history.sort(key=lambda daily_case: self.sort_daily_cases(daily_case, status_agg), reverse=True)
        countrires = map(lambda country_daily_case: country_daily_case.country_id,
                         countries_history[:data['limit']])

        countrySerializer = CountrySerializer(countrires, many=True)
        return Response(countrySerializer.data)

    def get_latest_country_daily_cases(self, country):
        try:
            return country.country_daily_cases.latest('created_at')
        except CountryDailyCases.DoesNotExist:
            return None

    def sort_daily_cases(self, daily_case, status_agg):
        if daily_case:
            return getattr(daily_case, status_agg)
        return 0


class SubscribtionViewSet(CreateAPIView):
    serializer_class = SubscribtionSerializer
    queryset = Country.subscription.through.objects.all()

    def post(self, request, *args, **kwargs):
        if 'country' not in request.data:
            return Response({'message': 'Country is required', 'error': False, 'code': 400},
                            status=status.HTTP_400_BAD_REQUEST)
        country = Country.objects.filter(name=request.data['country']).first()
        if not country:
            return Response({'message': 'Country not found', 'error': False, 'code': 400},
                            status=status.HTTP_400_BAD_REQUEST)
        request.data['country'] = country.id
        request.data['user'] = request.user.id
        return super().post(request, *args, **kwargs)
