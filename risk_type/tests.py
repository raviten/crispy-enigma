from django.core.urlresolvers import reverse
from risk_type.models import RiskType
from insurer.models import Insurer, User
from rest_framework.authtoken.models import Token
from risk_type.models import FieldType
from rest_framework.test import APITestCase
from django.test import Client
from risk_type.serializers import RiskTypeSerializer
from rest_framework import status
import json

# initialize the APIClient app
client = Client()


class RiskTypeFieldTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        self.insurer = Insurer.objects.create(user=user)
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

    def test_fail_create_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)
        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Construction Date',
                                      field_type='number')
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': '2018-02-23'}})
        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 400)

    def test_success_number_create_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)

        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Age of Property',
                                      field_type='number')
        risk_model.is_published = True
        risk_model.save()
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': 23}})
        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)

    def test_success_text_create_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)

        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Address',
                                      field_type='text')
        risk_model.is_published = True
        risk_model.save()
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': 'Heloooo'}})
        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)

    def test_success_date_create_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        local_value = '2018-01-01'
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)
        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Loan approval date',
                                      field_type='date')
        risk_model.is_published = True
        risk_model.save()

        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': local_value}})
        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)
        response = client.get(reverse('risk-list'),
                              content_type='application/json',
                              HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['risk_model'], risk_model.id)
        self.assertEqual(response.data[0]['data'][ft.name]['key'], ft.id)
        self.assertEqual(response.data[0]['data'][ft.name]['value'],
                         local_value)

    def test_success_enum_create_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        local_value = 1
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)

        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Bedrooms',
                                      field_type='enum')
        ft.schema = json.dumps({'oneOf': [1, 2, 3, 4]})
        ft.save()

        risk_model.is_published = True
        risk_model.save()

        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': local_value}})

        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)
        response = client.get(reverse('risk-list'),
                              content_type='application/json',
                              HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['risk_model'], risk_model.id)
        self.assertEqual(response.data[0]['data'][ft.name]['key'], ft.id)
        self.assertEqual(response.data[0]['data'][ft.name]['value'],
                         local_value)

    def test_failure_enum_create_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        local_value = 9
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)

        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Bedrooms',
                                      field_type='enum')
        ft.schema = json.dumps({'oneOf': [1, 2, 3, 4]})
        ft.save()

        risk_model.is_published = True
        risk_model.save()

        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': local_value}})

        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 400)

    def test_get_risk(self):
        '''
            Creating risk for un published risk_type
        '''
        user = User.objects.create(username='testuser')
        token = 'Token ' + Token.objects.create(user=user).key
        number_of_bed_rooms = 1
        risk_model = RiskType.objects.create(name='Property',
                                             insurer=self.insurer)

        ft = FieldType.objects.create(risk_model=risk_model,
                                      name='Bedrooms',
                                      field_type='enum')
        ft.schema = json.dumps({'oneOf': [1, 2, 3, 4]})
        ft.save()

        risk_model.is_published = True
        risk_model.save()

        data = {'risk_model': risk_model.id}
        data.update({ft.name: {'key': ft.id,
                               'value': number_of_bed_rooms}})
        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)
        response = client.get(reverse('risk-list'),
                              content_type='application/json',
                              HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['risk_model'], risk_model.id)
        self.assertEqual(response.data[0]['data'][ft.name]['key'], ft.id)
        self.assertEqual(response.data[0]['data'][ft.name]['value'],
                         number_of_bed_rooms)
        response = client.post(reverse('risk-list'),
                               json.dumps(data),
                               content_type='application/json',
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 201)
        response = client.get(reverse('risk-list'),
                              content_type='application/json',
                              HTTP_AUTHORIZATION=token)
        self.assertEqual(len(response.data), 2)
