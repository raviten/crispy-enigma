from django.contrib import admin

from risk_type.models import (
    RiskType,
    FieldType,
)
# Register your models here.

admin.site.register(RiskType)
admin.site.register(FieldType)
