from rest_framework.serializers import (IntegerField, CharField, Serializer, 
ModelSerializer, HyperlinkedIdentityField, SerializerMethodField)
from notes.models import Note

class NoteSerializer(ModelSerializer):
    author = SerializerMethodField(read_only=True)

    def get_author(self, obj):
        return str(obj.author.email)
        
    class Meta:
        model = Note
        fields = '__all__'


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail')

    class Meta:
        model = Note
        fields = ('id', 'title', 'url')
        
# class NoteSerializer(Serializer):
#     id = IntegerField(read_only=True)
#     title = CharField(required=True, max_length=250)
#     text = CharField(required=False, allow_blank=True)

#     def create(self, validated_data):
#         return Note.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance