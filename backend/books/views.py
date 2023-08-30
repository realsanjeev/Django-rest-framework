from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from books.models import Book
from books.serializers import BookSerializer
from books.permissions import IsStaffPermission
from books.pagination import CustomOffsetPagination

class BookAPIView(APIView, LimitOffsetPagination):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAdminUser, IsStaffPermission]
    pagination_class = CustomOffsetPagination

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Book.objects.none()
        return Book.objects.filter(user=user)
    
    def get_object(self, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return get_object_or_404(Book, pk=pk)
        return None

    def get(self, request, *args, **kwargs):
        self.serializer_context = {"request": request}
        instance = self.get_object(*args, **kwargs)
        
        # Initiate paginator in GET request
        paginatinator = CustomOffsetPagination()
        
        if not instance:
            queryset = Book.objects.all()
            result_page = paginatinator.paginate_queryset(queryset, request)
            serializer = BookSerializer(result_page, many=True, context=self.serializer_context)
            return paginatinator.get_paginated_response(serializer.data)
        
        serializer = BookSerializer(instance, context=self.serializer_context).data
        return Response({"detail": serializer})
    
    def post(self, request, *args, **kwargs):
        self.serializer_context = {"request": request}
        data = request.data
        serializer = BookSerializer(data=data, context=self.serializer_context)
        
        if serializer.is_valid(raise_exception=True):
            if not serializer.validated_data.get("desc"):
                serializer.validated_data["desc"] = serializer.validated_data["title"]
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        self.serializer_context = {"request": request}
        pk = kwargs.get("pk")
        instance = self.get_object(*args, **kwargs)
        
        if not instance:
            return Response({"message": f"Book with id: {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        serializer = BookSerializer(instance, data=data, context=self.serializer_context)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        self.serializer_context = {"request": request}
        instance = self.get_object(*args, **kwargs)
        pk = kwargs.get("pk")
        
        if not instance:
            return Response({"message": f"Record with book id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response({"detail": f"Book with id: {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
