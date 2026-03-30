from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    map_link = models.CharField(blank=True)
    price = models.IntegerField()
    description = models.TextField()
    #facilities as a checkbox
    wifi = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    
    
    
    
    image = models.ImageField(upload_to="rooms/", null=True, blank=True)
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='rooms', null=True)
    
    def __str__(self):
        return self.name

