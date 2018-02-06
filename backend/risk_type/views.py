from django.shortcuts import render


#  Authentication related imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets

from risk_type.serializers import RiskModelSerializer


# Create your views here.
class RiskModelViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = RiskModelSerializer

    def get_queryset(self):
        insurer = self.request.user.insurer
        queryset = insurer.risk_model.all()
        return queryset
