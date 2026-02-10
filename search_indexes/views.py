from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Q
from search_indexes.documents.ip import IpDocument
from search_indexes.serializers.ip import IPCheckSerializer
from search_indexes.documents.hash import HashDocument
from search_indexes.serializers.hash import HashCheckSerializer


class CheckIPAPIView(APIView):

    def get(self, request, format=None):
        ip = request.query_params.get("ip")
        if not ip:
            return Response({"error": "IP parameter is required"}, status=400)

        search = IpDocument.search().query(
            "bool",
            should=[
                {"term": {"value": ip}},
                {"wildcard": {"value": f"{ip}|*"}}
            ],
            minimum_should_match=1
        )

        result = search.execute()

        # ✅ If found
        if result.hits.total.value > 0:
            serializer = IPCheckSerializer(result.hits[0])
            data = serializer.data
            data["status"] = "malicious"
            return Response(data)

        # ✅ If NOT found
        return Response({
            "ip": ip,
            "status": "safe"
        })


class CheckHashAPIView(APIView):

    def get(self, request, format=None):
        hash = request.query_params.get("hash")
        if not hash:
            return Response({"error": "Hash parameter is required"}, status=400)

        search = HashDocument.search().query(
            "bool",
            should=[
                {"term": {"value": hash}},
                {"wildcard": {"value": f"{hash}|*"}}
            ],
            minimum_should_match=1
        )

        result = search.execute()

        # ✅ If found
        if result.hits.total.value > 0:
            serializer = IPCheckSerializer(result.hits[0])
            data = serializer.data
            data["status"] = "malicious"
            return Response(data)

        # ✅ If NOT found
        return Response({
            "hash": hash,
            "status": "safe"
        })



