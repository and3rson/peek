from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.utils.timezone import now
from django.db import transaction
from django.db.models import F
import models
import serializers
import redis
import json


class NotesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.NoteSerializer

    def _get_channel_name(self, user):
        return 'notifications-{}'.format(user.id)

    def _notify(self, user, data):
        client = redis.Redis()
        client.publish(self._get_channel_name(user), json.dumps(data))

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
        self._notify(self.request.user, dict(type='created', instance=serializer.data))

    def perform_update(self, serializer):
        serializer.save(updated=now())
        self._notify(self.request.user, dict(type='updated', instance=serializer.data))

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

    @list_route(methods=['GET'])
    def poll(self, request):
        client = redis.Redis(socket_timeout=10)
        ps = client.pubsub()
        ps.subscribe([self._get_channel_name(request.user)])

        result = []

        try:
            for item in ps.listen():
                if item['type'] == 'message':
                    ps.unsubscribe()
                    result.append(json.loads(item['data']))
                    break
        except redis.TimeoutError:
            pass

        return Response(dict(events=result))
