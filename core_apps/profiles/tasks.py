import base64
import logging
from uuid import UUID
from celery import shared_task
from .models import Profile
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


@shared_task(name="upload_avatar_to_s3")
def upload_avatar_to_s3(profile_id: UUID, image_content: str, filename: str) -> None:
    try:
        profile = Profile.objects.get(id=profile_id)

        # convert to image from Base64 string
        format, imgstr = image_content.split(";base64,")
        ext = format.split("/")[-1]
        decoded_file = base64.b64decode(imgstr)

        # creating ContentFile
        file_obj = ContentFile(decoded_file, name=filename)

        profile.avatar.save(filename, file_obj, save=True)
    except Profile.DoesNotExist:
        print(f"Profile with id {profile_id} not found.")
    except Exception as e:
        print(f"Error uploading avatar to S3: {str(e)}")


@shared_task(name="update_all_trust_scores")
def update_all_trust_scores():
    qs = Profile.objects.filter(user__is_active=True).iterator(chunk_size=100)

    count = 0
    for profile in qs:
        try:
            # Assumes update_trust_score() handles its own saving
            profile.update_trust_score()
            count += 1
            profile.save()
        except Exception as e:
            logger.error(f"Failed to update score for {profile.id}: {e}")

        logger.info(f"Updated trust scores for {count} profiles.")
