from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from books.serializers import BookSerializer
from books.models import Book

@api_view(['GET', 'POST'])
def book_details(request, *args, **kwargs):
    if request.method == 'GET':
        instance = Book.objects.all().order_by("?").first()
        if instance:
            serialize = BookSerializer(instance).data
            return Response(serialize)
        return Response({"error": "Book not found in the database!!!!"})

    elif request.method == 'POST':
        data = request.data
        print("*" * 43)
        print(data)
        serializer = BookSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            # serializer.save()
            return Response({"message": "successful valid post", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({"error": "Not valid input"})
