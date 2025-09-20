from django.core.management.base import BaseCommand
from django.conf import settings
import os
from e_mall.models.products import Products

class Command(BaseCommand):
    def handle(self, *args, **options):
        images_dir = settings.MEDIA_ROOT + '/uploads/products/'
        image_files = os.listdir(images_dir)
        image_names = []
        for img in Products.objects.all():
            image_names.extend([os.path.basename(img.image1.name),
                                os.path.basename(img.image2.name),
                                os.path.basename(img.image3.name),])
        
        special_images = ['logo.png','logo2.png','logo88.png']  # add your special images here
        orphaned_images_found=False
        for img in image_files:
            if os.path.basename(img) not in image_names and os.path.basename(img) not in special_images:
                try:
                    os.remove(images_dir + img)
                    print(f'Deleted orphaned image: {img}')
                    orphaned_images_found=True
                except PermissionError:
                    print(f'Permission denied for image: {img}')
        if not orphaned_images_found:
            print('no orphaned images found')