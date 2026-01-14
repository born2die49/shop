from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core_apps.common.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Profile(TimeStampedModel):
    # gender choice
    class Gender(models.TextChoices):
        MALE = "MALE", _("Male")
        FEMALE = "FEMALE", _("Female")
        OTHER = "OTHER", _("Other")

    # division choice for delivery calculation
    class Division(models.TextChoices):
        DHAKA = "DHAKA", _("Dhaka")
        CHATTOGRAM = "CHATTOGRAM", _("Chattogram")
        KHULNA = "KHULNA", _("Khulna")
        RAJSHAHI = "RAJSHAHI", _("Rajshahi")
        BARISHAL = "BARISHAL", _("Barishal")
        SYLHET = "SYLHET", _("Sylhet")
        RANGPUR = "RANGPUR", _("Rangpur")
        MYMENSINGH = "MYMENSINGH", _("Mymensingh")

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    
    # common fields
    avatar = models.ImageField(verbose_name=_("Avatar"),upload_to="avatars/", blank=True, null=True)
    gender = models.CharField(verbose_name=_("Gender"), choices=Gender.choices, default=None, null=True, max_length=20)
    bio = models.TextField(verbose_name=_("Bio"), blank=True, null=True, max_length=500)
    
    # contact and verification
    phone_number = PhoneNumberField(verbose_name=_("Phone Number"), max_length=30, db_index=True)
    is_phone_verified = models.BooleanField(verbose_name=_("Is Phone Verified"), default=False)
    
    # address
    address_line_1 = models.CharField(verbose_name=_("Address Line 1"), max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(verbose_name=_("Address Line 2"), max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name=_("City"), max_length=50, blank=True, null=True)
    thana = models.CharField(verbose_name=_("Thana/Upazila"), max_length=50, blank=True, null=True)
    division = models.CharField(verbose_name=_("Division"), choices=Division.choices, max_length=20, blank=True, null=True)
    country = CountryField(verbose_name=_("Country"), default="BD", blank=True, null=True)

    # customer trust score
    trust_score = models.IntegerField(verbose_name=_("Trust Score"), default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def is_complete(self):
        """checks if profile is complete"""
        required_fields = [self.gender, self.phone_number, self.address_line_1, self.city, self.division]
        return all(required_fields)
      
    @property
    def role(self):
        if self.user.is_superuser: return "ADMIN"
        if self.user.is_staff: return "STAFF"
        return "CUSTOMER"