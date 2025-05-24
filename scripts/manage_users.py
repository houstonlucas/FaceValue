#!/usr/bin/env python
"""
Script to clear non-superuser accounts and create test users via Django ORM.
"""
import os
import sys
import argparse

# Ensure project base directory is on path and settings are configured
def setup_django():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facevalue.settings')
    import django
    django.setup()


def clear_users():
    """Remove all users except superusers."""
    from django.contrib.auth.models import User
    non_super = User.objects.filter(is_superuser=False)
    count = non_super.count()
    non_super.delete()
    print(f"Deleted {count} non-superuser accounts.")


def create_users(usernames, password, role='User'):
    """Create test users with given usernames, password, and assign them a role."""
    from django.contrib.auth.models import User, Group
    for name in usernames:
        if User.objects.filter(username=name).exists():
            print(f"User '{name}' already exists, skipping.")
            continue
        user = User.objects.create_user(username=name, password=password)
        group = Group.objects.get(name=role)
        user.groups.add(group)
        print(f"Created user '{name}' with password '{password}' and assigned role '{role}'.")


def create_roles():
    """Define and set up roles (SuperAdmin, Admin, User) and their permissions."""
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    # Create groups
    superadmin_group, _ = Group.objects.get_or_create(name='SuperAdmin')
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    user_group, _ = Group.objects.get_or_create(name='User')

    # Assign permissions to groups
    # SuperAdmin permissions
    superadmin_permissions = [
        'add_user', 'change_user', 'delete_user',
        'add_group', 'change_group', 'delete_group',
    ]
    for perm in superadmin_permissions:
        permission = Permission.objects.get(codename=perm)
        superadmin_group.permissions.add(permission)

    # Admin permissions
    admin_permissions = [
        'delete_review', 'delete_comment',
    ]
    for perm in admin_permissions:
        permission = Permission.objects.get(codename=perm)
        admin_group.permissions.add(permission)

    # User permissions
    user_permissions = [
        'add_review', 'change_review', 'add_comment', 'change_comment',
    ]
    for perm in user_permissions:
        permission = Permission.objects.get(codename=perm)
        user_group.permissions.add(permission)

    # Ensure role hierarchy
    for perm in admin_group.permissions.all():
        superadmin_group.permissions.add(perm)
    for perm in user_group.permissions.all():
        admin_group.permissions.add(perm)


def assign_role(username, role_name):
    """Assign an existing user to a role group."""
    from django.contrib.auth.models import User, Group
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"No such user '{username}'.")
        return
    try:
        group = Group.objects.get(name=role_name)
    except Group.DoesNotExist:
        print(f"No such role '{role_name}'.")
        return
    user.groups.add(group)
    print(f"Assigned role '{role_name}' to user '{username}'.")


def main():
    parser = argparse.ArgumentParser(description='Manage user accounts')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('clear', help='Clear all non-superuser accounts')
    sub.add_parser('setup_roles', help='One-time setup of roles')

    create_parser = sub.add_parser('create', help='Create test users')
    create_parser.add_argument('--usernames', nargs='+', default=['testuser1', 'testuser2'],
                               help='List of usernames to create')
    create_parser.add_argument('--password', default='password123',
                               help='Password for created users')
    create_parser.add_argument('--role', default='User',
                               help='Role to assign to created users (default: User)')

    # Add assign_role command
    assign_parser = sub.add_parser('assign_role', help='Assign a role to an existing user')
    assign_parser.add_argument('username', help='Username to assign role')
    assign_parser.add_argument('role', help='Role name to assign')

    args = parser.parse_args()

    setup_django()

    if args.command == 'clear':
        clear_users()
    elif args.command == 'setup_roles':
        create_roles()
    elif args.command == 'create':
        create_users(args.usernames, args.password, args.role)
    elif args.command == 'assign_role':
        assign_role(args.username, args.role)


if __name__ == '__main__':
    main()
