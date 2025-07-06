from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Create an employee user for testing'

    def handle(self, *args, **options):
        # Create Employee group if it doesn't exist
        employee_group, created = Group.objects.get_or_create(name='Employee')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Employee group created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Employee group already exists')
            )

        # Create employee user
        employee_user, created = User.objects.get_or_create(
            username='employee',
            defaults={
                'email': 'employee@company.com',
                'first_name': 'John',
                'last_name': 'Employee',
                'is_staff': False,
                'is_superuser': False
            }
        )

        if created:
            employee_user.set_password('employee123')
            employee_user.save()
            employee_user.groups.add(employee_group)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Employee user created successfully!\n'
                    f'Username: {employee_user.username}\n'
                    f'Password: employee123\n'
                    f'Email: {employee_user.email}'
                )
            )
        else:
            # Update existing user
            employee_user.set_password('employee123')
            employee_user.save()
            employee_user.groups.add(employee_group)
            self.stdout.write(
                self.style.WARNING(
                    f'Employee user already exists, password updated!\n'
                    f'Username: {employee_user.username}\n'
                    f'Password: employee123\n'
                    f'Email: {employee_user.email}'
                )
            )

        # Verify the user can authenticate
        user = authenticate(username='employee', password='employee123')
        if user:
            self.stdout.write(
                self.style.SUCCESS('Authentication test passed!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('Authentication test failed!')
            ) 