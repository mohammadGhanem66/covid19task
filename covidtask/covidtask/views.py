from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,action
from .models import Country
from .serializers import CountrySerializer,SubscribtionSerializer
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.viewsets import ViewSetMixin,ViewSet
from rest_framework import views,status
from django.db.models import Count
from django.contrib.auth.models import User

class CountryViewSet(ViewSetMixin,ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    @action(detail=False,methods=('GET',),url_path="death-percentage")
    def get_percentage(self,request,*args,**kwargs):
        if 'country' not in request.query_params:
            return Response({'message': 'Missing parameters (country)', 'error': True, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        try:
            country = Country.objects.filter(name=request.query_params['country']).first()
            countrySerializer = CountrySerializer(country)
            deathCount = countrySerializer.data['death']
            confirmedCount = countrySerializer.data['confirmed']
            percentage = deathCount / confirmedCount
            responseData = {"death": deathCount, "confirmed": confirmedCount, "percentage": percentage}
            return Response(responseData)
        except:
            return Response()

    @action(detail=False, methods=('GET',), url_path="top")
    def get(self, request, *args, **kwargs):
        if 'status' not in request.query_params:
            return Response({'message': 'Missing parameters (status)', 'error': True, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)
        stauts = request.query_params['status']
        if 'limit' in request.query_params:
            limit = int(request.query_params['limit'])
        else:
            limit = 3

        countries = Country.objects.annotate(subscriptions_count=Count('subscription')).filter(subscriptions_count__gt =0 )\
            .all().order_by("-"+stauts)[:limit]

        countrySerializer = CountrySerializer(countries,many=True)
        return Response(countrySerializer.data)


class SubscribtionViewSet(ViewSet):
    def create(self,request,*args,**kwargs):
        serializer = SubscribtionSerializer(data={**request.data,"userId":request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'sucess','error':False,'code':201},status=status.HTTP_201_CREATED)


