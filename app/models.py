import os
from supabase import create_client
from django.conf import settings
from django.db import models


class ShimlaAttraction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="tmp/", blank=True, null=True)  # Image field is optional
    image_url = models.URLField(blank=True, null=True)  # Make image_url optional
    location = models.CharField(max_length=255, blank=True)
    opening_hours = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Step 1: Only proceed with custom save logic if an image is uploaded
        if self.image and hasattr(self.image, 'file'):
            # Initialize the Supabase client
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            bucket_name = "attractions"
            temp_path = f'/tmp/{self.image.name}'

            # Step 2: Save the image temporarily to a file
            with open(temp_path, 'wb') as temp_file:
                for chunk in self.image.chunks():
                    temp_file.write(chunk)

            # Step 3: Upload the image to Supabase
            with open(temp_path, 'rb') as temp_file:
                response = supabase.storage.from_(bucket_name).upload(self.image.name, temp_file)

            if response.error:
                raise Exception(f"Failed to upload image to Supabase: {response.error}")

            # Step 4: Save the public URL to the image_url field
            public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{response['path']}"
            self.image_url = public_url

            # Step 5: Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

        # Step 6: Call the original save method
        super().save(*args, **kwargs)
