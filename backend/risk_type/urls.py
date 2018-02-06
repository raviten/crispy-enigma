from django.shortcuts import render

# Create your views here.
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from risk_type.views import (
    RiskModelViewSet
)

router = DefaultRouter()
router.register(r'risk-model', RiskModelViewSet, 'risk-model')

urlpatterns = [
]
urlpatterns += router.urls
