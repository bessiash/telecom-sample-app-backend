from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from .models import Operator, Code, Phone, Purce


class PurceViewSet(generics.RetrieveAPIView):
    """
    API endpoint that allows purce to be viewed.
    """
    serializer_class = serializers.PurceSerializer
    
    def get_object(self):
        user = self.request.user
        obj =  Purce.objects.get(user=user)
        return obj
    

class OperatorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows operator to be viewed.
    """
    queryset = Operator.objects.all()
    serializer_class = serializers.OperatorSerializer
    
    @action(detail=True, methods=['post'])
    def refill(self, request, pk=None):
        user = request.user
        purce_obj, _ = Purce.objects.get_or_create(user=user)
        operator = self.get_object()
        phone = request.data['phone']
        amount = int(request.data['amount'])
        
        phone_is_valid = operator.check_phone(phone)
        if not phone_is_valid:
            data = {
                'error': 'You use incorrectly phone number'
            }
            return Response(data)
        
        amount_is_valid = amount >= 1 and amount <= 1000 and amount <= purce_obj.balance
        if not amount_is_valid:
            data = {
                'error': 'Incorrectly amount value'
            }
            return Response(data, status=500)
        
        with transaction.atomic():
            phone_obj, _ = Phone.objects.get_or_create(number=phone)
            
            phone_obj.balance += amount
            purce_obj.balance -= amount
            
            phone_obj.save()
            purce_obj.save()
        
        serializer = self.get_serializer(operator, many=False)
        return Response(serializer.data)
