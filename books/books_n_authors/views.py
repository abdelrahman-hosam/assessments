from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
import json
@api_view(['GET'])
def get_books(request):
    if request.method == 'GET':
        books = models.books.objects.all()
        serializer = serializers.book_serializer(books , many= True)
        return Response(serializer.data , status= status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_book_by_id(request , id):
    if request.method == 'GET':
        book = get_object_or_404(models.books , id= id)
        return Response({'id': book.id , 'title': book.book_name , 'price':book.price})
    return Response({'failure_message': 'we could not get the book'} , status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book(request):
    if request.method == 'POST':
            serializer = serializers.book_serializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success_message': 'The book was added' , 'book_title': serializer.data['book_name'] , 'book_id': serializer.instance.id})
    return Response({'failure_message':'the book was not added'})
@api_view(['DELETE' , 'GET'])
@permission_classes([IsAuthenticated])
def delete_book(request , id):
    if request.method == 'DELETE':
        book = get_object_or_404(models.books , id= id)
        book.delete()
        return Response({'success_message':'The book was deleted'})
    return Response({'failure_message':'The book was not deleted'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_book(request , id):
    if request.method == 'PUT':
        book = get_object_or_404(models.books , id= id)
        data = json.loads(request.body)
        book.book_name = data.get('book_name' , book.book_name)
        book.price = data.get('price' , book.price)
        book.authors.set(data.get('authors' , book.authors.all()))
        book.save()
        return Response({'succsses_message':'book was updated successfully'})
    return Response({'failure_message': 'book was not updated'})
@api_view(['GET'])
def get_authors(request):
    if request.method == 'GET':
        authors = models.authors.objects.all()
        return Response({'authors': list(authors)})
    return Response({'failure_message':'we could not retrieve all the authors'})
@api_view(['GET'])
def get_author(request , id):
    if request.method == 'GET':
        author = get_object_or_404(models.authors , id= id)
        if author:
            serializer = serializers.author_serializer(author)
            return Response({'author_name': serializer.data['author_name'] , 'author_books': serializer.data['books'] , 'author_id':serializer.data['id']})
    return Response({'failure_message':'we could not retrieve the author info'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_author(request):
    if request.method == 'POST':
        serializer = serializers.author_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success_message': 'author was added successfully' , 'author_id':serializer.instance.id})   
    return Response({'failure_message': 'author was not added or it is a get request'})
@api_view (['DELETE'])
@permission_classes([IsAuthenticated])
def delete_author(request , id):
    if request.method == 'DELETE':
        author = get_object_or_404(models.authors,id=id)
        author.delete()
        return Response({'success_message':'author was successfully deleted'})
    return Response({'failure_message':'we could not delete the user'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_author(request , id):
    if request.method == 'PUT':
        if request.method == 'PUT':
            author = get_object_or_404(models.authors , id= id)
            data = json.loads(request.body)
            author.author_name = data.get('author_name' , author.author_name)
            author.save()
            return Response({'succsses_message':'book was updated successfully'})
    return Response({'failure_message': 'book was not updated'})
@api_view(['GET'])
def search_library(request):
    data = request.query_params.get('search' , '')
    if data:    
        if request.method == 'GET':
            authors = models.authors.objects.filter(author_name= data).values('author_name')
            books = models.books.objects.filter(book_name= data).values('book_name')
            similar_results = similar(data)
            results = {
                'books': list(books),
                'authors': list(authors),
                'similar_results': similar_results
            }
            return Response({'search_results': results} , status= status.HTTP_200_OK)
    return Response({'failure_message': 'we could not retrieve the search results'} , status= status.HTTP_400_BAD_REQUEST)
def similar(data):
    similar_books = models.books.objects.filter(book_name__icontains= data).values('book_name')
    similar_authors = models.authors.objects.filter(author_name__icontains= data).values('author_name')
    similar_results = {
        'similar_authors': list(similar_authors), 
        'similar_books': list(similar_books)
    }
    return similar_results
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    if request.method == 'POST':
        serializer = serializers.favorites_serializer(data = request.data)
        if serializer.is_valid():
            books_ids = serializer.validated_data['favorites']
            user = request.user
            books_titles = []
            recommendations = []
            for book_id in books_ids:
                id = book_id.id
                if not user.favorites.filter(id= id).exists():
                    user.favorites.add(id)
                    print(user.favorites.all())
                    print(id)
                    books_titles.append(models.books.objects.get(id= id).book_name)
                    recommendations = models.books.objects.filter(tag= models.books.objects.get(models.books.objects.get(id= id).tag)).exclude(id__in= user.favorites.values_list , flat= True)          
                    return Response({'success_message':'favorite books were successfully added' , 'books': books_titles , 'recommendations':recommendations , 'favorites':user.favorites.all()})
    return Response({'failure_message':'we could not add those books to your favorites'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    user = request.user
    favorites = list(user.favorites.values_list('id' , flat= True))
    serializer = serializers.favorites_serializer(data= {'favorites':favorites})
    if serializer.is_valid():
        return Response({'favorites_list': favorites})
    return Response({'failure_message': 'sorry there is an error happened'})