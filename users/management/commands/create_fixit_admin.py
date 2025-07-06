from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Create the FixIT admin user'

    def handle(self, *args, **options):
        # Create IT Admin group if it doesn't exist
        admin_group, created = Group.objects.get_or_create(name='IT Admin')
        if created:
            self.stdout.write(
                self.style.SUCCESS('IT Admin group created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('IT Admin group already exists')
            )

        # Create FixIT admin user
        admin_user, created = User.objects.get_or_create(
            username='FixIT',
            defaults={
                'email': 'admin@fixit.com',
                'first_name': 'FixIT',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            admin_user.set_password('Zion1@mercy')
            admin_user.save()
            admin_user.groups.add(admin_group)
            self.stdout.write(
                self.style.SUCCESS(
                    f'FixIT admin user created successfully!\n'
                    f'Username: FixIT\n'
                    f'Password: Zion1@mercy\n'
                    f'Email: admin@fixit.com'
                )
            )
        else:
            # Update existing user
            admin_user.set_password('Zion1@mercy')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            admin_user.groups.add(admin_group)
            self.stdout.write(
                self.style.SUCCESS(
                    f'FixIT admin user updated successfully!\n'
                    f'Username: FixIT\n'
                    f'Password: Zion1@mercy\n'
                    f'Email: admin@fixit.com'
                )
            ) 