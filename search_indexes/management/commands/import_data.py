from django.core.management.base import BaseCommand
from search_indexes.models import IP, Hash
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
file_path_ip = BASE_DIR / "feeds" / "indicators_ip.jsonl"
file_path_hash = BASE_DIR / "feeds" / "indicators_hashes.jsonl"


class Command(BaseCommand):
    help = 'Import IP and Hash datasets from JSONL files'

    def handle(self, *args, **kwargs):
        # --- Import IPs ---
        with open(file_path_ip, 'r') as file:
            for line in file:
                data = json.loads(line)
                IP.objects.get_or_create(
                    value=data['value'],
                    type=data['type'],
                    country=data.get('country'),
                    feed_name=data.get('source', 'unknown')
                )
        self.stdout.write(self.style.SUCCESS('IPs imported successfully!'))

        # --- Import Hashes ---
        with open(file_path_hash, 'r') as file:
            for line in file:
                data = json.loads(line)
                Hash.objects.get_or_create(
                    value=data['value'],
                    type=data['type'],
                    country=data.get('country'),
                    feed_name=data.get('source', 'unknown')
                )
        self.stdout.write(self.style.SUCCESS('Hashes imported successfully!'))
