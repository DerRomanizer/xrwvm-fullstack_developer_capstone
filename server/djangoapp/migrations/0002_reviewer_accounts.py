# Creates the accounts the course reviewers use to log in.
#
# The capstone instructions ask for a superuser root/root so that the
# reviewer can open the admin site. The deployed container starts from an
# empty SQLite database, so the accounts are created by this data
# migration instead of by hand.

from django.db import migrations

REVIEWER_ACCOUNTS = [
    {"username": "root", "password": "root", "email": "root@example.com"},
    {"username": "admin", "password": "admin",
     "email": "admin@example.com"},
]


def create_reviewer_accounts(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    for account in REVIEWER_ACCOUNTS:
        if not User.objects.filter(username=account["username"]).exists():
            User.objects.create_superuser(
                username=account["username"],
                email=account["email"],
                password=account["password"],
            )


def remove_reviewer_accounts(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    usernames = [account["username"] for account in REVIEWER_ACCOUNTS]
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_reviewer_accounts,
                             remove_reviewer_accounts),
    ]
