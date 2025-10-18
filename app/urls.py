from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    CategoryViewSet,
    LocationViewSet,
    CommunityViewSet,
    CommunitySubmissionViewSet,
    NewsEventViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'submissions', CommunitySubmissionViewSet)
router.register(r'news', NewsEventViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('communities/', views.communities_list, name='communities'),
    path('community/<slug:slug>/', views.community_detail, name='community_detail'),
    path('submit-community/', views.submit_community, name='submit_community'),

    
    path("dashboard/", views.admin_dashboard, name="dashboard"),
    path("accounts/login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]

