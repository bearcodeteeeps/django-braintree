from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Import dict of plans from settings
        group_plans_dict = settings.BRAINTREE_PLAN_IDS

        # Make a list of all the groups. This loop is mainly used to
        # make new group records in the database
        group_list = []

        for tuple in group_plans_dict:
            group, created = Group.objects.get_or_create(name = group_plans_dict[tuple])
            group_list.append(group)
            group.save()

        if (getattr(settings, "BRAINTREE_EXCLUSIVE_GROUPS") != None):
            ex_group_names = settings.BRAINTREE_EXCLUSIVE_GROUPS
            ex_group = []

            for tuple in ex_group_names:
                group, created = Group.objects.get_or_create(name = tuple)
                group_list.remove(group)
                group.delete()
                group, created = Group.objects.get_or_create(name = "ex_" + tuple)
                print created
                group_list.append(group)
                group.save()

        # NOTE: Codename constructed from static string "payment."
        # which is the app name right now. If app name changes
        # change this as well. Find a way to make it change with
        # the app name
        for group in group_list:
            if group.name.find("ex_") > -1:
                permission_codename = group.name[3:]
            else:
                permission_codename = group.name
            group_permission = Permission.objects.get(codename = permission_codename)
            group.permissions.add(group_permission)
            group.save()

        self.stdout.write(self.style.SUCCESS('Successfully created groups!'))
