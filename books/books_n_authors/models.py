from django.db import models
from django.utils import timezone
class authors(models.Model):
    author_name = models.CharField(max_length= 250 , null= False , blank= False)
class books(models.Model):
    book_name = models.CharField(max_length=250 , blank= False , null= False)
    published_at = models.DateTimeField(default= timezone.now)
    price = models.FloatField(blank = False , null= False)
    authors = models.ManyToManyField(authors , related_name='books' , null= False)
    tag = models.CharField(max_length= 250 , null= False , blank= False)