import re
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

class Purce(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=10000)
    
    def __str__(self):
        return 'Purce ({0})'.format(self.user)


class Operator(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.name
    
    def check_phone(self, phone):
        codes = self.code_set.all()
        codes = '|'.join(code.value for code in codes)
        phone_reqexp = '\+7 \((?:' + codes + ')\) \d{3} \d{2} \d{2}'
        check = re.match(phone_reqexp, phone)
        return check is not None
    
    
class Code(models.Model):
    value = models.CharField(validators=[RegexValidator(regex='^[0-9]{3}$', message='Length has to be 3')], max_length=3, unique=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{0} ({1})'.format(self.operator, self.value)

    
class Phone(models.Model):
    number = models.CharField(
        validators=[RegexValidator(regex='^\+7 \(\d{3}\) \d{3} \d{2} \d{2}$', message='Incorrectly format of phone number')], 
        max_length=18, 
        unique=True
    )
    balance = models.FloatField(default=0, blank=False, null=False)
    
    def __str__(self):
        return self.number
