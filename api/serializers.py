from core.models import *
from accounts.models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Request
        fields = (
            'id',
            'title',
            'description',
            'branch',
            'semester',
            'date',
            'closing_response',
            "username",
            # 'upvotes',
            # 'downvotes'
        )

        read_only_fields = ("id", "responses", "username")

class FileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username')

    class Meta:
        model = File
        fields = (
            'id',
            'doc',
            'description',
            'branch',
            'semester',
            'upload_date',
            'request',
            # 'upvotes',
            # 'downvotes'
        )

        read_only_fields = ('id',)

class ReqDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    responses = FileSerializer(many=True, read_only=True)
    closing_response = FileSerializer(many=False, read_only=True)

    class Meta:
        model = Request
        fields = (
            'id',
            'title',
            'description',
            'branch',
            'semester',
            'date',
            'user',
            "username",
            'closing_response',
            # 'upvotes',
            # 'downvotes',
            'responses',
        )
        read_only_fields = ("responses", "username")

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.first_name')
    username = serializers.CharField(source='user.username')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = (
            'name',
            'username',
            'email',
            'avatar',
            'about',
            'website',
            'branch',
            'semester',
            'college',
            'date_joined',
        )
