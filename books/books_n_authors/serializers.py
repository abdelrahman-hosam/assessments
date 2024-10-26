from rest_framework import serializers
from . import models 
class book_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.books
        fields = ['book_name' , 'price' , 'authors' , 'tag']
class author_serializer(serializers.ModelSerializer):
    books = book_serializer(many= True , read_only= True)
    class Meta:
        model = models.authors
        fields = ['author_name', 'books']
class book_by_id_serializer(serializers.Serializer):
    book_name = serializers.CharField()
    price = serializers.FloatField()
    id = serializers.IntegerField()
    authors = serializers.ListField(child = serializers.PrimaryKeyRelatedField(queryset = models.authors.objects.all()) , min_length= 0)
    tag = serializers.CharField()
class favorites_serializer(serializers.Serializer):
    favorites = serializers.ListField(child = serializers.PrimaryKeyRelatedField(queryset = models.books.objects.all()) , min_length = 0)