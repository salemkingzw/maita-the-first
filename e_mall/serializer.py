from rest_framework import serializers
from e_mall.models.products import Products
from e_mall.models.userprofile import *
from e_mall.models.location import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']  # Exclude the password field
        depth = 1

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisements
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Location
        fields = '__all__'

#for product posting
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ['seller']

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    location = LocationSerializer()
    class Meta:
        model = Products
        fields = '__all__'
        depth=1



