from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
  first_name = serializers.ReadOnlyField(source="user.first_name")
  last_name = serializers.ReadOnlyField(source="user.last_name")
  username = serializers.ReadOnlyField(source="user.username")
  full_name = serializers.ReadOnlyField(source="user.get_full_name")
  country = CountryField(name_only=True)
  avatar = serializers.SerializerMethodField()
  date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
  
  class Meta:
    model = Profile
    fields = ["id", "first_name", "last_name", "username", "full_name", "gender", "country", "city", "bio", "date_joined", "avatar"]
    
  def get_avatar(self, obj: Profile) -> str | None:
    try:
      if obj.avatar:
        return obj.avatar.url
    except ValueError:
      pass
      return None

    
class UpdateProfileSerializer(serializers.ModelSerializer):
  first_name = serializers.CharField(source="user.first_name")
  last_name = serializers.CharField(source="user.last_name")
  username = serializers.CharField(source="user.username")
  country = CountryField(name_only=True)
  
  class Meta:
    model = Profile
    fields = ["first_name", "last_name", "username", "gender", "country", "city", "bio", "phone_number"]
    
  
class AvatarUploadSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ["avatar"]