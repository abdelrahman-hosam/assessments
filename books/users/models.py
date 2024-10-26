from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from books_n_authors.models import books
class library_user(AbstractBaseUser):
    username = models.CharField(max_length= 250 , blank= False , null= False , unique= True)
    password = models.CharField(max_length=128 , blank= False , null= False)
    favorites = models.ManyToManyField(books , related_name= 'users_favorites')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
