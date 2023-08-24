from rest_framework.routers import Response

from books.models import Book

def book_details(request, *args, **kwargs):
    instance = Book.objects.all().order_by("?").first()
    data = {}
    if instance:
    
        return Response(data)
    return Response({"error": "Book not found in database!!!!"})