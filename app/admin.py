
from django.contrib import admin
from .models import (
    Category, Location, Community, CommunitySubmission, NewsEvent
)

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


# Location Admin
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country')
    search_fields = ('name', 'region', 'country')
    list_filter = ('country',)
    prepopulated_fields = {"slug": ("name", "country")}


# Community Admin
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'approved', 'category', 'location', 'founded_date', 'added_at')
    list_filter = ('status', 'approved', 'category', 'location')
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = 'added_at'


# CommunitySubmission Admin with approval action
@admin.register(CommunitySubmission)
class CommunitySubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'approved', 'submitted_at', 'category', 'location', 'community')
    list_filter = ('approved', 'category', 'location')
    search_fields = ('name', 'description')
    actions = ['approve_selected_submissions']

    def approve_selected_submissions(self, request, queryset):
        count = 0
        for submission in queryset:
            if not submission.approved:
                submission.approve_submission()
                count += 1
        self.message_user(request, f"{count} submission(s) approved and linked to new Community entries.")
    approve_selected_submissions.short_description = "Approve selected submissions and create Communities"


# NewsEvent Admin
@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'source_url')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'published_at'
