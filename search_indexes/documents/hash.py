from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from search_indexes.models import Hash

# Name of the Elasticsearch index got from the settings
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,  # can be 1 but 0 is enough for this project
)


@INDEX.document
class HashDocument(Document):
    """Minimal IP Elasticsearch document."""

    value = fields.KeywordField()  # exact match search only

    class Django:
        model = Hash
        fields = []  # no other fields needed

