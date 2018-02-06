from django.contrib import admin

from risk_type.models import (
    RiskModel,
    GenericFieldType,
)
# Register your models here.

admin.site.register(RiskModel)
admin.site.register(GenericFieldType)
