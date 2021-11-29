from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Problem, CodeImage, Reply, Comment
from .serializers import ProblemSerializer, ReplySerializer, CommentSerializer
from .permissions import IsAuthorPermission


# class ProblemListView(ListAPIView):
#     queryset = Problem.objects.all()
#     serializer_class = ProblemListSerializer
#
# class ProblemCreateView(CreateAPIView):
#     queryset = Problem
#     serializer_class = ProblemCreateSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}

class PermissionMixin:
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProblemViewSet(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
