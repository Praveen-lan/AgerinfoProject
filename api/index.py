import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agerinfo_backend.settings')

import django
django.setup()

from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=0)

from django.contrib.auth.models import User
if not User.objects.filter(username='admin@agerinfo.com').exists():
    user = User.objects.create_superuser('admin@agerinfo.com', 'admin@agerinfo.com', 'admin123')
    from rest_framework.authtoken.models import Token
    Token.objects.create(user=user)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application
