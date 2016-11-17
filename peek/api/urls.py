from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from peek.notes import viewsets


router = DefaultRouter()
router.register('notes', viewsets.NotesViewSet, base_name='note')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
