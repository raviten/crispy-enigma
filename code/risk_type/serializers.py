from rest_framework import serializers
from risk_type.models import (
    RiskType,
    FieldType,
    Risk
)
import json


class FieldTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldType
        fields = ('ordering', 'name', 'field_type', 'id', 'schema')

    # Converting schema from string to json and json to string
    def to_representation(self, instance):
        ret = super(FieldTypeSerializer,
                    self).to_representation(instance)
        ret['schema'] = json.loads(ret['schema'])
        return ret

    def to_internal_value(self, data):
        # change to below some point
        data['schema'] = json.dumps(data['schema'])
        ret = super(FieldTypeSerializer, self).to_internal_value(data)
        return ret


class RiskTypeSerializer(serializers.ModelSerializer):
    field_types = FieldTypeSerializer(many=True,
                                      read_only=True)

    class Meta:
        model = RiskType
        fields = ('field_types', 'name', 'id')


class RiskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def run_validatiors(self, value):
        print(value)
        super(RiskSerializer, self).run_validatiors(value)

    def create(self, validated_data):
        print(validated_data)
        # instance, _ = Risk.objects.get_or_create(**validated_data)
        return None

    class Meta:
        model = Risk
        fields = '__all__'
