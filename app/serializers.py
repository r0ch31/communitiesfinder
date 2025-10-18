from rest_framework import serializers
from .models import Category, Location, Community, CommunitySubmission, NewsEvent

# ----------------------
# Category Serializer
# ----------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_approved']
        read_only_fields = ['slug']


# ----------------------
# Location Serializer
# ----------------------
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'region', 'country', 'slug']
        read_only_fields = ['slug']


# ----------------------
# Community Serializer
# ----------------------
class CommunitySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'location',
            'founded_date', 'added_at', 'approved', 'website', 'facebook_page', 'status'
        ]
        read_only_fields = ['slug', 'added_at']


# ----------------------
# Community Submission Serializer
# ----------------------
class CommunitySubmissionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    community = CommunitySerializer(read_only=True)

    class Meta:
        model = CommunitySubmission
        fields = [
            'id', 'name', 'description', 'category', 'location', 'founded_date',
            'website', 'facebook_page', 'submitted_at', 'approved', 'community'
        ]
        read_only_fields = ['submitted_at']


# ----------------------
# News/Event Serializer
# ----------------------
class NewsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsEvent
        fields = [
            'id', 'title', 'slug', 'content', 'published_at', 'image', 'source_url'
        ]
        read_only_fields = ['slug', 'published_at']
