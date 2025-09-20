from django.db import models 
  
  
class Category(models.Model): 
    name = models.CharField(max_length=50) 
    verbose_name = models.CharField(max_length=50, blank=True, default='')
  
    @staticmethod
    def get_all_categories(): 
        return Category.objects.all() 
  
    def __str__(self): 
        return self.verbose_name if self.verbose_name else self.name 