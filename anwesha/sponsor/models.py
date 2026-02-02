from django.db import models
from user.models import User


class MyntraRegistration(models.Model):
    """
    Tracks users who registered via Myntra sponsor form.
    Synced from Google Sheets periodically.
    """
    anwesha_user_id = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_synced = models.DateTimeField(auto_now=True)
    
    # Store raw data from sheet if needed
    raw_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Myntra Registration"
        verbose_name_plural = "Myntra Registrations"
    
    @property
    def anwesha_user(self):
        """Get the related User object"""
        if self.anwesha_user_id:
            try:
                return User.objects.get(anwesha_id=self.anwesha_user_id)
            except User.DoesNotExist:
                return None
        return None
    
    def __str__(self):
        return f"{self.email} - {self.anwesha_user_id or 'No User'}"


# Sponsors Model Definition
class Sponsors(models.Model):
    # Fields to store sponsor information
    sponsor_name = models.CharField(max_length=50, unique=True)  # Name of the sponsor (Max 50 characters)

    sponsor_phone_number = models.CharField(max_length=15, unique=True)  # Phone number of the sponsor (Max 15 characters)

    sponsor_description = models.CharField(max_length=1000, blank=True, null=True)  # Description of the sponsor (optional)

    order = models.IntegerField(default=0)  # Order in which the sponsors are displayed (default: 0)

    sponsor_email = models.EmailField(unique=True)  # Email address of the sponsor (unique)

    sponsor_logo = models.ImageField(blank=True, null=True, upload_to="static/sponsor_logo")  # Sponsor's logo image

    sponsor_link = models.URLField(null=True, blank=True)  # Website link of the sponsor (optional)

    sponsor_instagram_id = models.CharField(max_length=255, blank=True, null=True)  # Instagram ID of the sponsor (optional)

    sponsor_facebook_id = models.CharField(max_length=255, blank=True, null=True)  # Facebook ID of the sponsor (optional)

    sponsor_linkdin_id = models.CharField(max_length=255, blank=True, null=True)  # LinkedIn ID of the sponsor (optional)

    def __str__(self):
        return self.sponsor_name

    class Meta:
        verbose_name_plural = "Sponsors"  # Plural name for the model in the admin interface
        verbose_name = "Sponsor"  # Singular name for the model in the admin interface
