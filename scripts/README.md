# Useful scripts for managing the repository

## Managing Users
### manage_users.py
A script to clear non-superuser accounts and create test users.

Usage:
```bash
# Clear all non-superuser users
env/bin/python manage_users.py clear

# Create test users with default usernames (testuser1, testuser2) and password
env/bin/python manage_users.py create

# Create custom test users
env/bin/python manage_users.py create --usernames alice bob --password ComplexPass123
```
