# core/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Sample

class Command(BaseCommand):
    help = 'Create admin and user groups with permissions'

    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='admin')
        user_group, _ = Group.objects.get_or_create(name='user')

        sample_ct = ContentType.objects.get_for_model(Sample)
        permissions = Permission.objects.filter(content_type=sample_ct)
        admin_group.permissions.set(permissions)
        admin_group.save()

        view_permission = Permission.objects.get(codename='view_sample')
        user_group.permissions.add(view_permission)
        user_group.save()

        self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully.'))
