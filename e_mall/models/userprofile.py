from django.contrib.auth.models import User 
from django.db import models 
from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.base import ContentFile

class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    about = models.CharField( 
        max_length=250, default='', blank=True, null=True)

    def __str__(self): 
        return self.about 
    
class ProfileFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
    
    def follow(self, user):
        ProfileFollow.objects.get_or_create(follower=self, followed=user)
    def unfollow(self, user):
        ProfileFollow.objects.get(follower=self, followed=user).delete()
    
    def __str__(self): 
        return str(self.follower)

class SubscriptionPlan(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    post_limit=models.IntegerField()
    def __str__(self):
        return str(self.name)

class Subscription(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    is_active=models.BooleanField(default=True)
    plan=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)+str(" active") if self.is_active is True else str(self.user) + str(" expired")
    


    
class Advertisements(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=100)
    link=models.CharField(max_length=300)
    image = models.ImageField(upload_to='uploads/top_advertisement/', default='uploads/top_advertisement/logo.png')

    def save(self, *args, **kwargs):
        if self.image:
            self.image=self.compress_image(self.image) 
        super().save(*args, **kwargs)

    def compress_image(self, image):
        img = Image.open(image)
        img=img.convert('RGB')
        #skip compression if there already is an image in the field, genius        
        if 'top_advertisement/' in image.url:
            return image
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
        new_image=ContentFile(im_io.getvalue(), image.name)

        return new_image

    def __str__(self):
        return str(self.title)