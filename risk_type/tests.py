from django.core.urlresolvers import reverse
from risk_type.models import RiskType
from insurer.models import Insurer, User
from rest_framework.authtoken.models import Token
from risk_type.models import FieldType
from rest_framework.test import APITestCase
from django.test import Client
from risk_type.serializers import RiskTypeSerializer
from rest_framework import status


# initialize the APIClient app
client = Client()


class RiskTypeFieldTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        self.insurer = Insurer.objects.create(user=user)
        self.token = 'Token ' + Token.objects.create(user=user).key
        risk_model = RiskType.objects.create(name='Car',
                                             insurer=self.insurer)
        risk_model = RiskType.objects.create(name='House',
                                             insurer=self.insurer)
        # Adding generic field types
        FieldType.objects.create(risk_model=risk_model,
                                 name='Name',
                                 field_type='text')
        FieldType.objects.create(risk_model=risk_model,
                                 name='Construction Date',
                                 field_type='date')

        FieldType.objects.create(risk_model=risk_model,
                                 name='Construction Date',
                                 field_type='number')
        FieldType.objects.create(risk_model=risk_model,
                                 name='Construction Date',
                                 field_type='enum')
        # Publishing risk model
        risk_model.is_published = True

    def test_risk_models(self):
        risk_model = self.insurer.risk_model.get(name='House')
        self.assertEqual(risk_model.name, 'House', 'Should be name')

    def test_get_risk_models(self):
        # get API response
        response = client.get(reverse('risk-type-list'))
        # get data from db
        risk_types = RiskType.objects.filter(is_published=True)
        serializer = RiskTypeSerializer(risk_types, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
