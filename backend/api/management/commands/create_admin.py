from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create an admin user for AGERinfo'

    def add_arguments(self, parser):
        parser.add_argument('--email', default='admin@agerinfo.com', help='Admin email')
        parser.add_argument('--password', default='admin123', help='Admin password')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        username = email

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password(password)
            user.save()
            Token.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {email}'))
        else:
            self.stdout.write(f'User {email} already exists')
