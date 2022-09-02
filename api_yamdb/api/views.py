from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ParseError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Comment, Genre, Review, Title
from core.filters import TitleFilter
from core.permissions import (IsAdminOrSuperuserOrReadOnly,
                              IsAuthorOrStaffOrReadOnly)
from .mixins import ListCreateDestroyViewSet
from .serializers import (CategoriesSerializer,
                          CommentsSerializer,
                          GenreSerializer,
                          ReviewsSerializer,
                          TitlesCreateSerializer,
                          TitlesSerializer)


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrSuperuserOrReadOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrSuperuserOrReadOnly, )
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrSuperuserOrReadOnly, )
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filterset_class = TitleFilter
    ordering_fields = ('category', 'genre', 'name', 'year')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializer
        return TitlesCreateSerializer


class ReviewsViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        if review.title != title:
            raise ParseError(detail='Не совпадают ID ревью и Тайтла',
                             code=status.HTTP_400_BAD_REQUEST)
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        if review.title != title:
            raise ParseError(detail='Не совпадают ID ревью и Тайтла',
                             code=status.HTTP_400_BAD_REQUEST)
        serializer.save(author=self.request.user, review=review)
