from eph_calendar.models import RegisteredDate
from rest_framework import serializers


class RegisteredDateDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredDate
        fields = "__all__"


class RegisteredDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredDate
        fields = ["title", "date"]
