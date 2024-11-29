import os
from supabase import create_client
from django.conf import settings
from django.db import models

# Get the base directory of your project
BASE_DIR = settings.BASE_DIR

class ShimlaAttraction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=settings.DOWNLOAD_PATH)  # Django admin file upload
    image_url = models.URLField(blank=True, null=True)  # Make image_url optional
    location = models.CharField(max_length=255, blank=True)
    opening_hours = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Step 1: Check if the image is being uploaded (this check ensures it's not just an update)
        if hasattr(self.image, 'file') and self.image:
            # Initialize the Supabase client
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            bucket_name = "attractions"
            temp_path = f'/tmp/{self.image.name}'

            # Step 2: Save the image temporarily to the /tmp directory
            with open(temp_path, 'wb') as temp_file:
                for chunk in self.image.chunks():
                    temp_file.write(chunk)
            
            # Step 3: Upload the image to Supabase
            with open(temp_path, 'rb') as temp_file:
                response = supabase.storage.from_(bucket_name).upload(self.image.name, temp_file)
            try: 
                public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{response.full_path}"
                self.image_url = public_url  # Save the URL to the image_url field
            except:
                raise Exception(f"Failed to upload image to Supabase: {response.error}")
            
            # Step 5: Clean up the temporary file
        
        super().save(*args, **kwargs)  # Call the original save method
        # full_path = f"{BASE_DIR}{temp_path}"
        # print(full_path,temp_path)
        # if os.path.exists(temp_path):
        #     print("==============")
        #     os.remove(full_path)  # Remove the temporary file after upload
