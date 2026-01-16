import requests
from django.core.files.base import ContentFile
from core_apps.profiles.models import Profile


def save_profile(backend, user, response, *args, **kwargs):
  if backend.name == "google-oauth2":
    avatar_url = response.get("picture", None)
    if avatar_url:
      try:
        image_response = requests.get(avatar_url)
        if image_response.status_code == 200:
          profile, created = Profile.objects.get_or_create(user=user)
          filename = f"avatar_{user.username}.jpg"
          file_obj = ContentFile(image_response.content)
          profile.avatar.save(filename, file_obj, save=True)
      except Exception as e:
        print(f"Error saving avatar from Google: {str(e)}")