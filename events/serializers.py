from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):  # Class X must implement all abstract methods

    class Meta:
        model = Event
        fields = ['id', 'title', 'status']

