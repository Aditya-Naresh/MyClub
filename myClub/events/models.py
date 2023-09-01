from django.db import models

# Venue 
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code =models.CharField('Zip Code', max_length=10)
    phone = models.CharField('Contact Phone', max_length=15)
    website = models.URLField('Website Address')
    email_address = models.EmailField('Email Address') 


    def __str__(self):
        return self.name
    

# User
class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
    

# Event
class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue  =models.CharField('Venue', max_length=120)
    manager = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser)


    def __str__(self):
        return self.name
