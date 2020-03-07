from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import TweetViewSet, AnnotationViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'annotations', AnnotationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
