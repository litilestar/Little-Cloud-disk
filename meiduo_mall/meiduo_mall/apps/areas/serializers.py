from rest_framework import serializers

from .models import Area

class AresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id','name')

class SubsAresSerializer(serializers.ModelSerializer):
    subs = AresSerializer(many=True,read_only=True)
    class Meta:
        model = Area
        fields = ('id','name','subs')