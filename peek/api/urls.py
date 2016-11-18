from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from peek.notes import viewsets


router = DefaultRouter()
router.register('notes', viewsets.NotesViewSet, base_name='note')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', views.obtain_auth_token),
]
