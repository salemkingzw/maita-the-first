from django.db import models 
from .category import Category 
from .location import Location 
from django.contrib.auth.models import User 
from django.utils.text import slugify
import uuid
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings 
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.core.files.uploadedfile import InMemoryUploadedFile

class Products(models.Model): 
    name = models.CharField(max_length=60)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    price = models.CharField(max_length=12,default='',blank=True, null=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    description = models.TextField( 
        max_length=1000, default='', blank=True, null=True) 
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default='', blank=True, null=True)
    phone_no = models.CharField(max_length=15, default='', blank=True, null=True)
    image1 = CloudinaryField('image',null=True,blank=True)
    #image1 = models.ImageField(upload_to='uploads/products/', default='uploads/products/logo.png')
    image2 = CloudinaryField('image',default='',null=True,blank=True)
    image3 = CloudinaryField('image',default='',null=True,blank=True)
    image4 = CloudinaryField('image',default='',null=True,blank=True)
    image5 = CloudinaryField('image',default='',null=True,blank=True)
    image6 = CloudinaryField('image',default='',null=True,blank=True)
    image7 = CloudinaryField('image',default='',null=True,blank=True)
    image8 = CloudinaryField('image',default='',null=True,blank=True)
    image9 = CloudinaryField('image',default='',null=True,blank=True)
    image10 = CloudinaryField('image',default='',null=True,blank=True)
    international = models.BooleanField(blank=True, null=True, default=False)

    @property
    def image_url(self):
        if self.image1:
            return self.image1.url
        return "https://res.cloudinary.com/diovsna1y/image/upload/v1756129362/logo_bgsqwu.png"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=self.generate_unique_slug()        
        
        if self.image1 and not hasattr(self.image1, 'url'):  # only compress new uploads
            self.image1 = self.compress_image(self.image1)
        
        if self.image2 and not hasattr(self.image2, 'url'):  # only compress new uploads
            self.image2 = self.compress_image(self.image2)

        if self.image3 and not hasattr(self.image3, 'url'):  # only compress new uploads
            self.image3 = self.compress_image(self.image3)
        
        if self.image4 and not hasattr(self.image4, 'url'):  # only compress new uploads
            self.image4 = self.compress_image(self.image4)

        if self.image5 and not hasattr(self.image5, 'url'):  # only compress new uploads
            self.image5 = self.compress_image(self.image5)

        if self.image6 and not hasattr(self.image6, 'url'):  # only compress new uploads
            self.image6 = self.compress_image(self.image6)
        
        if self.image7 and not hasattr(self.image7, 'url'):  # only compress new uploads
            self.image7 = self.compress_image(self.image7)

        if self.image8 and not hasattr(self.image8, 'url'):  # only compress new uploads
            self.image8 = self.compress_image(self.image8)

        if self.image9 and not hasattr(self.image9, 'url'):  # only compress new uploads
            self.image9 = self.compress_image(self.image9)

        if self.image10 and not hasattr(self.image10, 'url'):  # only compress new uploads
            self.image10 = self.compress_image(self.image10)
            
        super().save(*args, **kwargs)   
    
    def generate_unique_slug(self):
        uuid_str = uuid.uuid4().hex[:8]
        return f"{slugify(self.name)}-{uuid_str}"
    
    def compress_image(self, image):
        img = Image.open(image)
        img=img.convert('RGB')
        #skip compression if there already is an image in the field, genius        
        #if 'products/' in image.url:
        #    return image
        #rotation and orientation from EXIF data
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            exif = img.getexif()
            if exif is not None:
                exif = dict(exif.items())
                orientation=exif.get(orientation, None)

                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)            
        except(AttributeError,KeyError,IndexError):
            pass
        #resize image if too large        
        max_size=(800,800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        im_io=BytesIO()
        img.save(im_io, 'JPEG', quality=70)
        im_io.seek(0)
        return InMemoryUploadedFile(
        im_io, None, image.name, 'image/jpeg', im_io.getbuffer().nbytes, None
        )
    
    def get_absolute_url(self):
        return reverse('e_mall:products_id', args=[str(self.slug)])

    @staticmethod
    def get_products_by_id(ids): 
        return Products.objects.filter(id__in=ids) 
  
    @staticmethod
    def get_all_products(): 
        return Products.objects.all() 
  
    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        if category_id: 
            return Products.objects.filter(category=category_id) 
        else: 
            return Products.get_all_products()
        
    def __str__(self): 
        return self.name 
