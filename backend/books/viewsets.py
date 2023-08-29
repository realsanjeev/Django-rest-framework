from rest_framework import viewsets, mixins

from books.models import Book
from books.serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    '''
    Viewset combine logic of differrent viewss in single class.

    get -> `list`  -> queryset
    get -> `retrieve` -> Model instance
    post -> `create` -> New instance
    put -> `Update`
    patch -> `Partial update`
    delete -> `destroy`
    '''
    queryset = Book.objects.all()
    lookup_field = "pk"
    serializer_class = BookSerializer

class BookGenericViewsets(viewsets.GenericViewSet):
    '''
    get -> `list`  -> queryset
    get -> `retrieve` -> Model instance
    '''
    serializer_class = BookSerializer
    lookup_field = "pk"
    queryset = Book.objects.all()
