# Create your views here.
from rest_framework.routers import DefaultRouter
from risk_type.views import (
    RiskTypeViewSet,
    RiskViewSet
)

router = DefaultRouter()
router.register(r'risk-type', RiskTypeViewSet, 'risk-type')
router.register(r'risk', RiskViewSet, 'risk')

urlpatterns = [
]
urlpatterns += router.urls
