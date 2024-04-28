from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile for existing Users'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user).save()