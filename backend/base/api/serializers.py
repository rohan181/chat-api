from rest_framework.serializers import ModelSerializer
from base.models import Note,video


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class videoSerializer(ModelSerializer):
    class Meta:
        model =video
        fields = '__all__'
