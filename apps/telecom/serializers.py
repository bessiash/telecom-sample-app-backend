from rest_framework import serializers

from .models import Operator, Code, Purce

class PurceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Purce
        fields = ('balance',)


class CodeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.value        
     
        
class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    code_set = CodeField(many=True, read_only=True)
    
    class Meta:
        model = Operator
        fields = ('id', 'name', 'code_set')