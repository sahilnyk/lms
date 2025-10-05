from django.core.management.base import BaseCommand
from django.db import transaction
from academics.models import Course, Lesson
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed academics with courses and lessons (simple)"

    def add_arguments(self, parser):
        parser.add_argument("--lessons", type=int, default=100)
        parser.add_argument("--courses", type=int, default=10)
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        fake = Faker()
        total = options["lessons"]
        num_courses = max(1, options["courses"])
        if options["clear"]:
            Lesson.objects.all().delete()
            Course.objects.all().delete()
            self.stdout.write("Cleared existing data")

        courses = []
        with transaction.atomic():
            for _ in range(num_courses):
                courses.append(Course.objects.create(
                    title=fake.sentence(nb_words=4).rstrip("."),
                    description=fake.paragraph(nb_sentences=2),
                ))
            per_course = max(1, total // num_courses)
            created = 0
            for c in courses:
                for pos in range(1, per_course + 1):
                    if created >= total:
                        break
                    Lesson.objects.create(
                        course=c,
                        title=fake.sentence(nb_words=6).rstrip("."),
                        content=fake.paragraph(nb_sentences=3),
                        position=pos,
                        is_done=False,
                    )
                    created += 1
            while created < total:
                c = random.choice(courses)
                pos = c.lessons.count() + 1
                Lesson.objects.create(
                    course=c,
                    title=fake.sentence(nb_words=6).rstrip("."),
                    content=fake.paragraph(nb_sentences=3),
                    position=pos,
                    is_done=False,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {total} lessons across {num_courses} courses"))