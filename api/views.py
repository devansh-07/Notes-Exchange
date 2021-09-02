from rest_framework import mixins
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.shortcuts import get_list_or_404, get_object_or_404

from .serializers import *
from core.models import File, Request
from django.contrib.auth import get_user_model

User = get_user_model()

# Get list of requests and Post a new request
class ListRequestView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = RequestSerializer

    def get_queryset(self):
        queryset = Request.objects

        usr = self.request.query_params.get('user')
        sem = self.request.query_params.get('semester')
        branch = self.request.query_params.get('branch')

        if usr is not None:
            queryset = queryset.filter(user__username=usr)

        if sem is not None:
            queryset = queryset.filter(semester=sem)

        if branch is not None:
            queryset = queryset.filter(branch=branch)

        return queryset.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, **kwargs):
        user = serializer.context['request'].user
        serializer.save(user=user)

# Get details of a particular request
class GetRequestDetailView(generics.RetrieveAPIView):
    serializer_class = ReqDetailSerializer
    queryset = Request.objects.all()
    lookup_field = "id"

# Get a list of Files
class ListFileView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = FileSerializer

    def get_queryset(self):
        queryset = File.objects

        usr = self.request.query_params.get('user')
        req = self.request.query_params.get('for_request')
        sem = self.request.query_params.get('semester')
        branch = self.request.query_params.get('branch')

        if usr is not None:
            queryset = queryset.filter(user__username=usr)

        if req is not None:
            queryset = queryset.filter(request=req)

        if sem is not None:
            queryset = queryset.filter(semester=sem)

        if branch is not None:
            queryset = queryset.filter(branch=branch)

        return queryset.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

# Get a single File
class GetFileView(generics.RetrieveAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    lookup_field = 'id'

# Add a new response to a particular request
class NewResponseView(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        generics.GenericAPIView
    ):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = FileSerializer

    def get_queryset(self):
        req_id = self.kwargs.get('id')
        r = Request.objects.filter(id=req_id)

        if not r.first():
            return r

        return r.first().responses

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, **kwargs):
        user = serializer.context['request'].user
        serializer.save(user=user)

# Get Profile Details
class ProfileDetailView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        uname = self.kwargs.get('username')
        profile = get_object_or_404(Profile, user__username=uname)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)
