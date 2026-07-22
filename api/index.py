import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agerinfo_backend.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

app = application
