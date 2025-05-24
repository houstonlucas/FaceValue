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


def create_users(usernames, password):
    """Create test users with given usernames and password."""
    from django.contrib.auth.models import User
    for name in usernames:
        if User.objects.filter(username=name).exists():
            print(f"User '{name}' already exists, skipping.")
            continue
        user = User.objects.create_user(username=name, password=password)
        print(f"Created user '{name}' with password '{password}'.")


def main():
    setup_django()
    parser = argparse.ArgumentParser(description='Manage user accounts')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('clear', help='Clear all non-superuser accounts')

    create_parser = sub.add_parser('create', help='Create test users')
    create_parser.add_argument('--usernames', nargs='+', default=['testuser1', 'testuser2'],
                               help='List of usernames to create')
    create_parser.add_argument('--password', default='password123',
                               help='Password for created users')

    args = parser.parse_args()

    if args.command == 'clear':
        clear_users()
    elif args.command == 'create':
        create_users(args.usernames, args.password)

if __name__ == '__main__':
    main()
