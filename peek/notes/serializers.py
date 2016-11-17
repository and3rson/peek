from rest_framework import serializers
import models


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = (
            'id', 'url',
            'body',
            'order',
            'color',
            'created',
            'updated'
        )
        read_only_fields = (
            'id', 'url',
            'order',
            'created',
            'updated',
        )

    def validate_color(self, value):
        if not value or len([c for c in value if c.upper() in '0123456789ABCDEF']) != 6:
            raise serializers.ValidationError('Invalid color provided. Example: "FF1177"')
        return value.upper()
