from rest_framework.routers import DefaultRouter
from books.viewsets import BookViewSet

router = DefaultRouter()
router.register("", viewset=BookViewSet, basename='books')

urlpatterns = router.urls
