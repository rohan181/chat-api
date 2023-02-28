from rest_framework.serializers import ModelSerializer
from base.models import *


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class videoSerializer(ModelSerializer):
    class Meta:
        model =video
        fields = '__all__'


class userprofileseriasilser(ModelSerializer):
    class Meta:
        model =video
        fields = '__all__'