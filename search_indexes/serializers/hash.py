from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from search_indexes.documents.hash import HashDocument


class HashCheckSerializer(DocumentSerializer):
    hash = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        document = HashDocument
        fields = (
            'hash',
            'status',
            'value',
            'type',
            'first_seen',
            'country',
            'feed_name',
        )

    def get_hash(self, obj):
        if obj:
            return obj.value
        return self.context.get('hash')

    def get_status(self, obj):
        return "malicious" if obj else "safe"
