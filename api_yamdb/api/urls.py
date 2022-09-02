from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet,
                    CommentsViewSet,
                    GenreViewSet,
                    ReviewsViewSet,
                    TitlesViewSet)

app_name = 'api'

api_router_v1 = DefaultRouter()
api_router_v1.register('categories',
                       CategoriesViewSet,
                       basename='categories')
api_router_v1.register('genres',
                       GenreViewSet,
                       basename='genres')
api_router_v1.register('titles',
                       TitlesViewSet,
                       basename='titles')
api_router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews')
api_router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include('users.urls', namespace='users')),
    path('v1/', include(api_router_v1.urls)),
]
