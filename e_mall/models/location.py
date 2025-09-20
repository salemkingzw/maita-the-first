from django.db import models 

class Country(models.Model): 
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=3,default='', blank=True, null=True)   

    def __str__(self): 
        return self.name   
  
class Location(models.Model): 
    name = models.CharField(max_length=50)  
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default='', blank=True, null=True) 

    def __str__(self): 
        return self.name 