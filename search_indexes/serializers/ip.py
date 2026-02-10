from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from search_indexes.documents.ip import IpDocument


class IPCheckSerializer(DocumentSerializer):
    ip = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        document = IpDocument
        fields = ('ip', 'status', 'value', 'type', 'first_seen', 'country', 'feed_name')

    def get_ip(self, obj):
        if obj:
            # Split by | if it exists
            return obj.value.split('|')[0]
        return self.context.get('ip')

    def get_status(self, obj):
        return "malicious" if obj else "safe"

