from .models import *
from rest_framework import serializers

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            'title',
            'description',
            'branch',
            'semester',
            'date',

            'closing_response',
            'user',

            'upvotes',
            'downvotes'
        )
        read_only_fields = ("user",)


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = (
            'doc',
            'description',
            'branch',
            'semester',
            'upload_date',

            'user',
            'request',

            'upvotes',
            'downvotes'
        )
