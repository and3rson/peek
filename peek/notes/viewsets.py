from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.utils.timezone import now
from django.db import transaction
from django.db.models import F
import models
import serializers


class NotesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        return models.Note.objects.filter(
            owner=self.request.user
        ).order_by('-order')

    def _get_max_order(self):
        newest_note = models.Note.objects.filter(
            owner=self.request.user
        ).order_by('-order').first()
        if newest_note:
            return newest_note.order
        else:
            return 0

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, order=self._get_max_order() + 1)

    def perform_update(self, serializer):
        serializer.save(updated=now())

    @detail_route(methods=['POST'])
    def move(self, request, pk):
        note = self.get_object()
        try:
            to = int(self.request.POST.get('to'))
        except:
            raise ValidationError('Missing "to" argument.')
        if to < 1:
            raise ValidationError('Positive number required for "to" argument.')
        with transaction.atomic():
            other = models.Note.objects.filter(
                owner=self.request.user,
                order=to
            ).first()
            if not other:
                to = self._get_max_order() + 1
            models.Note.objects.filter(
                owner=self.request.user,
                order__gte=to
            ).update(
                order=F('order') + 1
            )
            note.order = to
            note.save()
        return Response(status=201)
