
from rest_framework import serializers
from django_reclass.models import Reclass, ReclassTemplate


class ReclassTemplateSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        try:
            args[0].get_content()
        except Exception as e:
            raise e
        super(ReclassTemplateSerializer, self).__init__(*args, **kwargs)

    class Meta:

        model = ReclassTemplate


class ReclassSerializer(serializers.ModelSerializer):

    #    def to_representation(self, obj):
    #        return {
    #            'score': obj.score,
    #            'player_name': obj.player_name
    #        }

    class Meta:

        model = Reclass
