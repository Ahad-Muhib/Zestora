from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userprofile.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile for all existing users'

    def handle(self, *args, **kwargs):
        users_without_profile = []
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                users_without_profile.append(user.username)
        
        if users_without_profile:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created profiles for {len(users_without_profile)} users: {", ".join(users_without_profile)}'
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS('All users already have profiles!'))
