import os
import django
from django.urls import resolve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

try:
    match = resolve('/ai-chat/response/')
    print(f"Match found: {match.url_name} in {match.func}")
except Exception as e:
    print(f"Error resolving URL: {e}")
