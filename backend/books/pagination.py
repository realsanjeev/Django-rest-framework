from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "count": self.count,
            "results": data
        })
    