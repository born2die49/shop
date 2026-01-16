from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()

class CreateCustomerSerializer(UserCreateSerializer):
  class Meta(UserCreateSerializer.Meta):
    model = User
    fields = ["id", "username", "email", "first_name", "last_name", "password"]
  
class CustomUserSerializer(UserSerializer): 
  full_name = serializers.ReadOnlyField(source="get_full_name")
  gender = serializers.ReadOnlyField(source="profile.gender")
  # slug = serializers.ReadOnlyField(source="profile.slug")
  # occupation = serializers.ReadOnlyField(source="profile.occupation")
  phone_number = PhoneNumberField(source="profile.phone_number")
  country = CountryField(source="profile.country")
  city = serializers.ReadOnlyField(source="profile.city")
  avatar = serializers.ImageField(source="profile.avatar", read_only=True)
  trust_score = serializers.ReadOnlyField(source="profile.trust_score")
  
  class Meta(UserSerializer.Meta):
    model = User
    fields = [
      "id", "email", "first_name", "last_name", "username", "full_name", "gender", "phone_number", "country", "city", "trust_score", "avatar", "date_joined",
    ]
    read_only_fields = ["id", "email", "date_joined"]