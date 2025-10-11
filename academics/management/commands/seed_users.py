from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker
import random
import re

User = get_user_model()

def clean_part(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

class Command(BaseCommand):
    help = "Create teacher and student users with Indian names and name-based usernames/emails (no 'teacher'/'student' prefixes)."

    def add_arguments(self, parser):
        parser.add_argument("--teachers", type=int, default=10, help="Number of teacher users to create")
        parser.add_argument("--students", type=int, default=100, help="Number of student users to create")
        parser.add_argument("--password", type=str, default="password123", help="Password for all created users")
        parser.add_argument("--clear", action="store_true", help="Remove users in Teachers/Students groups before creating")

    def handle(self, *args, **options):
        fake = Faker("en_IN")
        num_teachers = options["teachers"]
        num_students = options["students"]
        pwd = options["password"]
        clear = options["clear"]

        teachers_group, _ = Group.objects.get_or_create(name="Teachers")
        students_group, _ = Group.objects.get_or_create(name="Students")

        if clear:
            qs = User.objects.filter(groups__name__in=["Teachers", "Students"]).distinct()
            pks = list(qs.values_list('pk', flat=True))
            count = len(pks)
            if pks:
                User.objects.filter(pk__in=pks).delete()
            self.stdout.write(f"Cleared {count} users from Teachers/Students groups")

        domains = ["gmail.com", "yahoo.in", "outlook.com", "hotmail.com"]

        def make_unique_email(base, domain):
            email = f"{base}@{domain}"
            suffix = 1
            while User.objects.filter(email=email).exists():
                email = f"{base}{suffix}@{domain}"
                suffix += 1
            return email

        def make_unique_username(base):
            uname = base
            suffix = 1
            while User.objects.filter(username=uname).exists():
                uname = f"{base}{suffix}"
                suffix += 1
            return uname

        created = {"teachers": 0, "students": 0}

        for _ in range(num_teachers):
            name = fake.name()
            parts = name.split(" ", 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ""
            base = clean_part(f"{first}.{last}" if last else first)
            if not base:
                base = clean_part(fake.user_name())
            domain = random.choice(domains)
            email = make_unique_email(base, domain)
            username = make_unique_username(base)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=pwd,
                first_name=first,
                last_name=last,
            )
            user.is_staff = True
            user.save()
            user.groups.add(teachers_group)
            created["teachers"] += 1

        for _ in range(num_students):
            name = fake.name()
            parts = name.split(" ", 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ""
            base = clean_part(f"{first}.{last}" if last else first)
            if not base:
                base = clean_part(fake.user_name())
            domain = random.choice(domains)
            email = make_unique_email(base, domain)
            username = make_unique_username(base)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=pwd,
                first_name=first,
                last_name=last,
            )
            user.is_staff = False
            user.save()
            user.groups.add(students_group)
            created["students"] += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created['teachers']} teachers and {created['students']} students. Default password: {pwd}"
        ))