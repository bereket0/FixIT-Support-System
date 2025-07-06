from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tickets.models import Ticket
from tips.models import TechTip
from quiz.models import Quiz

class Command(BaseCommand):
    help = 'Set up initial groups and permissions for FixIT system'

    def handle(self, *args, **options):
        # Create groups
        it_admin_group, created = Group.objects.get_or_create(name='IT Admin')
        employee_group, created = Group.objects.get_or_create(name='Employee')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created groups: IT Admin, Employee')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Groups already exist')
            )
        
        # Get content types
        ticket_ct = ContentType.objects.get_for_model(Ticket)
        techtip_ct = ContentType.objects.get_for_model(TechTip)
        quiz_ct = ContentType.objects.get_for_model(Quiz)
        
        # Get all permissions for each model
        ticket_permissions = Permission.objects.filter(content_type=ticket_ct)
        techtip_permissions = Permission.objects.filter(content_type=techtip_ct)
        quiz_permissions = Permission.objects.filter(content_type=quiz_ct)
        
        # Assign permissions to IT Admin group (all permissions)
        it_admin_group.permissions.set(
            list(ticket_permissions) + list(techtip_permissions) + list(quiz_permissions)
        )
        
        # Assign permissions to Employee group (view only)
        employee_group.permissions.set(
            list(ticket_permissions.filter(codename='view_ticket')) +
            list(techtip_permissions.filter(codename='view_techtip')) +
            list(quiz_permissions.filter(codename='view_quiz'))
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up permissions for all groups')
        ) 