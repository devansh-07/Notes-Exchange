from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins

from .serializers import FileSerializer, RequestSerializer
from .models import File, Request

class TestView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, **kwargs):
        user = serializer.context['request'].user
        serializer.save(user=user)

class RequestListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = RequestSerializer
    queryset = Request.objects.all()
