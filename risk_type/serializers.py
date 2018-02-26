from rest_framework import serializers
from risk_type.models import (
    RiskType,
    FieldType,
    Risk
)
import json
import numbers
import dateutil.parser as dp


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

    # Converting data from string to json and json to string
    def to_representation(self, instance):
        ret = super(RiskSerializer,
                    self).to_representation(instance)
        ret['data'] = json.loads(ret['data'])
        ret['name'] = instance.risk_type.name
        return ret

    def validate_field(self, field_type, value):
        e = ['This field is required']
        if not value or not isinstance(value, dict) or 'value' not in value:
            return {
                field_type.name: {
                    'key': field_type.id,
                    'value': e
                }}
        v = value['value']
        e = ['This field should be %s' % (field_type.field_type)]
        if field_type.field_type == 'number':
            valid_number = isinstance(v, numbers.Number)
            if not valid_number:
                return {field_type.name: {
                    'key': field_type.id,
                    'value': e
                }}
        elif field_type.field_type == 'text':
            valid_string = isinstance(v, str)
            if not valid_string:
                return {field_type.name: {
                    'key': field_type.id,
                    'value': e
                }}
        elif field_type.field_type == 'enum':
            one_of = json.loads(field_type.schema)['oneOf']
            e = ['field value should be one of ' + repr(one_of)]
            valid_one_of = v in one_of
            if not valid_one_of:
                return {field_type.name: {
                    'key': field_type.id,
                    'value': e
                }}
        elif field_type.field_type == 'date':
            try:
                dp.parse(v)
            except Exception as e:
                return {field_type.name: {
                    'key': field_type.id,
                    'value': ['Please enter valid date in ISO format']
                }}

    def validate(self, value):
        data = self.initial_data
        risk_type = value['risk_type']
        if not risk_type.is_published:
            raise serializers.ValidationError('Invalid risk type')
        d = {}
        errors = {}
        for field_type in risk_type.field_types.all():
            v = data.get(field_type.name, None)
            error = self.validate_field(field_type, v)
            if error:
                errors.update(error)
            else:
                d.update({field_type.name: v})
        if errors:
            raise serializers.ValidationError(repr(errors))
        value.update({'data': json.dumps(d)})
        return value

    def create(self, validated_data):
        instance = Risk.objects.create(**validated_data)
        return instance

    class Meta:
        model = Risk
        fields = '__all__'
