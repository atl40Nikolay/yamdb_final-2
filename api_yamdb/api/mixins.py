from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet


class ListCreateDestroyViewSet(GenericViewSet, ListModelMixin,
                               CreateModelMixin, DestroyModelMixin):
    """ViewSet для отображения списка, создания и удаления ресурса"""
    pass


class RetriveUpdateViewSet(GenericViewSet, RetrieveModelMixin,
                           UpdateModelMixin):
    """ViewSet для отображение и редактированного ресурса"""
    pass
