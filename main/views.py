from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Problem, CodeImage
from .serializers import ProblemListSerializer, ProblemCreateSerializer


class ProblemListView(ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemListSerializer

class ProblemCreateView(CreateAPIView):
    queryset = Problem
    serializer_class = ProblemCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}

