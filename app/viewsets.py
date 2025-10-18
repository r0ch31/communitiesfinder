from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from .models import Category, Location, Community, CommunitySubmission, NewsEvent
from .serializers import (
    CategorySerializer, LocationSerializer, CommunitySerializer,
    CommunitySubmissionSerializer, NewsEventSerializer
)

# Only use SearchFilter (no django-filter dependency)
filter_backends = [filters.SearchFilter]


# ----------------------
# Category ViewSet
# ----------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
    filter_backends = filter_backends
    search_fields = ['name']


# ----------------------
# Location ViewSet
# ----------------------
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
    filter_backends = filter_backends
    search_fields = ['name', 'region', 'country']


# ----------------------
# Community ViewSet
# ----------------------
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
    filter_backends = filter_backends
    search_fields = ['name', 'description']


# ----------------------
# Community Submission ViewSet
# ----------------------
class CommunitySubmissionViewSet(viewsets.ModelViewSet):
    queryset = CommunitySubmission.objects.all()
    serializer_class = CommunitySubmissionSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    filter_backends = filter_backends
    search_fields = ['name', 'description']


# ----------------------
# News/Event ViewSet
# ----------------------
class NewsEventViewSet(viewsets.ModelViewSet):
    queryset = NewsEvent.objects.all()
    serializer_class = NewsEventSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
    filter_backends = filter_backends
    search_fields = ['title', 'content']
