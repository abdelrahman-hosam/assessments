from django.urls import path
from . import views
urlpatterns = [
    path('' , views.get_books),
    path('books/favorites/add' , views.add_to_favorites),
    path('books/favorites', views.get_favorites),
    path('books/get/<int:id>' , views.get_book_by_id),
    path('books/add' , views.add_book),
    path('books/edit/<int:id>' , views.edit_book),
    path('books/delete/<int:id>' , views.delete_book),
    path('author/' , views.get_authors),
    path('author/add' , views.add_author),
    path('author/<int:id>' , views.get_author),
    path('author/delete/<int:id>' , views.delete_author),
]
