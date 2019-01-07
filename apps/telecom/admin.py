from django.contrib import admin

from .models import Operator, Code, Phone, Purce

class CodeInline(admin.TabularInline):
    model = Code
    extra = 0
    
    
@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    inlines = [
        CodeInline,
    ]
    
    
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Purce)
class PurceAdmin(admin.ModelAdmin):
    pass