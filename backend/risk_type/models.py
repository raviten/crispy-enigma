from django.db import models
from insurer.models import Insurer
# Create your models here.


class RiskModel(models.Model):
    insurer = models.ForeignKey(Insurer,
                                related_name='risk_model',
                                on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    version = models.IntegerField()
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class GenericFieldType(models.Model):
    risk_model = models.ForeignKey(RiskModel,
                                   related_name='field_types',
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    FIELD_TYPE_CHOICES = (
        ('text', 'text'),
        ('number', 'number'),
        ('date', 'date'),
        ('enum', 'enum'),
    )
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    ordering = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    # Validators gt, gte, lt, lte, eq, neq, is_one_of
    validators = models.TextField(default='{}')

    def __str__(self):
        return ('-').join([self.name])


# class Validator(models.Model):
#     generic_field_type = models.ForeignKey(GenericFieldType,
#                                            on_delete=models.CASCADE)
#     VALIDATOR_CHOICES = (
#         ('>', 'greaterthan'),
#         ('<', 'lessthan'),
#         ('>=', 'greaterthan_or_equal'),
#         ('<=', 'lessthan_or_equal'),
#         ('==', 'equals'),
#         ('!=', 'not_equals'),
#         ('equals', 'text_equals'),
#         ('is_one_of', 'enum_validator'),
#     )
#     operator = models.CharField(max_length=50, choices=VALIDATOR_CHOICES)
#     # value will be parsed based on field type.
#     # If enum everything will be loaded to array and will be cross verified
#     value = models.TextField()

#     def __str__(self):
#         return self.operator + self.value


# More generic Enum validation
# class EnumValidator(models.Model):
#     generic_field_type = models.ForeignKey(GenericFieldType,
#                                            on_delete=models.CASCADE)
#     ENUM_FIELD_TYPE_CHOICES = (
#         ('T', 'text'),
#         ('N', 'number'),
#         ('D', 'date'),
#     )
#     # By default displayname will be same as value
#     display_name = models.TextField()
#     # value will be parsed based on field type
#     value = models.TextField()
#     value_type = models.Choices(max_length=20,
#                                 choices=ENUM_FIELD_TYPE_CHOICES)
