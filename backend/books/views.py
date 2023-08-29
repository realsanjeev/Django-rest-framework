from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from books.permissions import IsStaffPermission
from books.serializers import BookSerializer
from books.models import Book

class BookAPIView(APIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAdminUser, IsStaffPermission]

    def get_queryset(self):
        return Book.objects.all()
    
    def get_object(self, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return get_object_or_404(Book, pk=pk)
        return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        if not instance:
            queryset = self.get_queryset()
            serializer = BookSerializer(queryset, many=True).data
            return Response({"books_list": serializer}, status=status.HTTP_200_OK)
        serializer = BookSerializer(instance).data
        return Response({"detail": serializer})
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if not serializer.validated_data.get("desc"):
                serializer.validated_data["desc"] = serializer.validated_data["title"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        instance = self.get_object(*args, **kwargs)
        if not instance:
            return Response({
                "message": f"Book with id: {pk} doesnot exist"
            }, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        pk = kwargs.get("pk")
        if not instance:
            return Response({"message": f"Record with book id: {pk} Not found"}, 
                            status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({
            "detail": f"Book with id: {pk} sucessfully deleted"
        }, status=status.HTTP_204_NO_CONTENT)
