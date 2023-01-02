from rest_framework.response import Response
from .models import Country, CountryDailyCases
from .serializers import CountrySerializer, SubscribtionSerializer, CountryViewSerializer, AggregatedCountriesSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import views, status
from django.db.models import Count
from django.db.models import Sum
from django.db.models import F


class CountryPercentageView(views.APIView):

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
            death_count = country.country_daily_cases.aggregate(Sum('death'))
            confirmed_count = country.country_daily_cases.aggregate(Sum('confirmed'))
            confirmed_count = confirmed_count['confirmed__sum']
            death_count = death_count['death__sum']
            if not confirmed_count:
                return Response({'message': 'Confirmed cant be zero', 'error': False, 'code': 500},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            percentage = death_count / confirmed_count
            response_data = {"death": death_count, "confirmed": confirmed_count, "percentage": percentage}
        else:
            response_data = {"death": 0, "confirmed": 0, "percentage": 0}
        return Response(response_data)


class TopCountryView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def get(self, request, *args, **kwargs):
        country_view_serializer = CountryViewSerializer(data=request.query_params)
        country_view_serializer.is_valid(raise_exception=True)
        data = country_view_serializer.validated_data
        status_values = ['death', 'confirmed', 'recoverd']
        if data['status'] not in status_values:
            return Response({'message': 'Wrong status', 'error': False, 'code': 400},
                            status=status.HTTP_400_BAD_REQUEST)
        subscribed_countries = Country.objects.annotate(subscriptions_count=Count('subscription')) \
            .filter(subscriptions_count__gt=0).values_list('id', flat=True)
        countrires = CountryDailyCases.objects.values('country_id', 'country_id__name').annotate(
            total=Sum(data['status'])).filter(
            country_id__in=subscribed_countries).order_by('-total')[:data['limit']]
        countrires = countrires.annotate(name=F('country_id__name'))

        aggregatedCountrySerializer = AggregatedCountriesSerializer(countrires, many=True)
        return Response(aggregatedCountrySerializer.data)


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
