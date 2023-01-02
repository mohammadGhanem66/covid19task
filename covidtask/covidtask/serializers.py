from rest_framework import serializers
from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class SubscribtionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country.subscription.through
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = instance.country.name
        data['user'] = instance.user.username
        return data


class CountryViewSerializer(serializers.Serializer):
    status = serializers.CharField()
    limit = serializers.IntegerField(default=3)


class AggregatedCountriesSerializer(serializers.Serializer):
    country_id = serializers.IntegerField()
    name = serializers.CharField()
    total = serializers.IntegerField()
