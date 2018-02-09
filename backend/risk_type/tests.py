from django.test import TestCase
from django.core.urlresolvers import reverse
from risk_type.models import RiskModel
from insurer.models import Insurer, User
from rest_framework.authtoken.models import Token
from risk_type.models import GenericFieldType
from rest_framework.test import APITestCase


class RiskModelFieldTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.token = Token.objects.create(user=self.user)
        insurer = Insurer.objects.create(user=self.user)
        risk_model = RiskModel.objects.create(name='house',
                                                   insurer=insurer,
                                                   version=1)
        GenericFieldType.objects.create(risk_model=risk_model,
                                        name='Name',
                                        field_type='text')
        GenericFieldType.objects.create(risk_model=risk_model,
                                        name='Construction Date',
                                        field_type='date')

        GenericFieldType.objects.create(risk_model=risk_model,
                                        name='Construction Date',
                                        field_type='number')
        GenericFieldType.objects.create(risk_model=risk_model,
                                        name='Construction Date',
                                        field_type='enum')
        self.api_authentication()
        self.url = '/api/risk-model'
        print(self.url)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_risk_model_create(self):
        response = self.client.get('/api/model-view/')
        print(response)
