from rest_framework import serializers
from risk_type.models import (
    RiskModel,
    GenericFieldType
)
import json


class GenericFieldTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFieldType
        fields = ('ordering', 'name', 'field_type', 'id', 'validators')

    def to_representation(self, instance):
        ret = super(GenericFieldTypeSerializer,
                    self).to_representation(instance)
        ret['validators'] = json.loads(ret['validators'])
        return ret

    def to_internal_value(self, data):
        # change to below some point
        data['validators'] = json.dumps(data['validators'])
        ret = super(GenericFieldTypeSerializer, self).to_internal_value(data)
        return ret


class RiskModelSerializer(serializers.ModelSerializer):
    field_types = GenericFieldTypeSerializer(many=True,
                                             read_only=True)

    class Meta:
        model = RiskModel
        fields = ('field_types', 'name', 'id')
