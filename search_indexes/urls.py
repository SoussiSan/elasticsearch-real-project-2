from django.urls import path
from search_indexes.views import CheckIPAPIView, CheckHashAPIView


urlpatterns = [
    path("check-ip/", CheckIPAPIView.as_view(), name="check-ip"),
    path("check-hash/", CheckHashAPIView.as_view(), name="check-hash"),
]

