from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import api


router = DefaultRouter()
router.register(r'operator', api.OperatorViewSet)

urlpatterns = [
    re_path(r'^purce/$', api.PurceViewSet.as_view(), name='purce'),
    path(r'', include(router.urls)),
]