from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category, Location, Community, CommunitySubmission, NewsEvent

# Base mixin for admin styling and access control
class AdminMixin:
    template_name_prefix = 'admin/'  # e.g., admin/community_list.html

# Community Views
class CommunityListView(AdminMixin, ListView):
    model = Community

class CommunityCreateView(AdminMixin, CreateView):
    model = Community
    fields = '__all__'
    success_url = reverse_lazy('admin_community_list')

class CommunityUpdateView(AdminMixin, UpdateView):
    model = Community
    fields = '__all__'
    success_url = reverse_lazy('admin_community_list')

class CommunityDeleteView(AdminMixin, DeleteView):
    model = Community
    success_url = reverse_lazy('admin_community_list')

# Repeat for other models...

class CategoryListView(AdminMixin, ListView):
    model = Category

class CategoryCreateView(AdminMixin, CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('admin_category_list')

# Add Location, Submission, NewsEvent similarly
