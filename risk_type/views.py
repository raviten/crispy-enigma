from django.shortcuts import get_object_or_404

from rest_framework import viewsets

#  Authentication related imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from risk_type.serializers import RiskTypeSerializer, RiskSerializer
from risk_type.models import RiskType


# Create your views here.
class RiskTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RiskTypeSerializer

    def get_queryset(self):
        queryset = RiskType.objects.filter(is_published=True)
        return queryset


class RiskViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = RiskSerializer

    def get_queryset(self):
        user = self.request.user
        return user.risks.all()
