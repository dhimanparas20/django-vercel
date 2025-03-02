import os
from supabase import create_client
from django.conf import settings
from django.db import models


class ShimlaAttraction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="media/images", blank=True, null=True)  # Image field is optional
    location = models.CharField(max_length=255, blank=True)
    opening_hours = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_public_image_url(self):
        if self.image:
            # Fetch Supabase project ID and bucket name from environment variables
            supabase_project_id = settings.SUPABASE_PROJECT_ID
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            return f"https://{supabase_project_id}.supabase.co/storage/v1/object/public/{bucket_name}/{self.image}"
        return None