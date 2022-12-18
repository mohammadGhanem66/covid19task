from rest_framework import serializers
from .models import Country
from django.contrib.auth.models import User

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class SubscribtionSerializer(serializers.Serializer):
    countries = serializers.ListField(child =serializers.CharField())
    userId = serializers.IntegerField()
    def create(self,validated_data):
        user = User.objects.get(id=validated_data['userId'])
        countries = Country.objects.filter(name__in=validated_data['countries']).all()
        for country in countries:
            user.subscriptions.add(country)
        user.save()
        return user;


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True,source="subscriptions")
    class Meta:
        model = User
        fields = ['id','username','country']