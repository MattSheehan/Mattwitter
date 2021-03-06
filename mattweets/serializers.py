'''
COPYRIGHT Matt Sheehan 2021
'''
from rest_framework import serializers
from .models import Tweet
from django.conf import settings
'''
Serializers:
Allow complex data such as querysets and model instances to be converted to 
native Python datatypes that can then be easily rendered into JSON, XML or other content types.

Deserializers:
Allows parsed data to be converted back into complex types, after first validating the incoming data.

ModelSerializers
provides a useful shortcut for creating serializers that deal with model instances and querysets.
'''
MAX_LENGTH = settings.MAX_LENGTH


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_LENGTH:
            raise serializers.ValidationError("Tweet is too long")
        return value
