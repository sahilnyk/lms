from django.core.management.base import BaseCommand
from django.db import transaction
from academics.models import Course, Lesson
from faker import Faker

RELEVANT_COURSES = [
    {
        "title": "Introduction to Computer Science",
        "description": "Fundamentals of computing, algorithms and problem solving.",
        "lessons": [
            "What is Computer Science?",
            "Algorithms & Pseudocode",
            "Basic Data Types",
            "Control Flow",
            "Functions and Procedures",
            "Basic Data Structures",
            "Complexity & Big-O",
            "Debugging Techniques",
            "Version Control (git)",
            "Next Steps & Resources",
        ],
    },
    {
        "title": "Programming in Python",
        "description": "Core Python language features and practical programming.",
        "lessons": [
            "Python setup & REPL",
            "Variables and Types",
            "Control Flow in Python",
            "Functions and Modules",
            "Data Structures: lists & tuples",
            "Dictionaries & Sets",
            "File I/O",
            "Error Handling",
            "Iterators & Generators",
            "Virtualenv & Packaging",
        ],
    },
    {
        "title": "Data Structures & Algorithms",
        "description": "Common data structures and algorithm design techniques.",
        "lessons": [
            "Arrays and Linked Lists",
            "Stacks and Queues",
            "Trees and Binary Trees",
            "Graphs Basics",
            "Searching & Sorting",
            "Hashing and Dictionaries",
            "Recursion & Divide & Conquer",
            "Greedy Algorithms",
            "Dynamic Programming",
            "Algorithm Analysis",
        ],
    },
    {
        "title": "Databases & SQL",
        "description": "Relational databases, SQL and basic database design.",
        "lessons": [
            "Introduction to Databases",
            "Basic SELECT queries",
            "Filtering and Sorting",
            "JOINs",
            "Aggregations & GROUP BY",
            "Indexes and Performance",
            "Transactions & Concurrency",
            "Schema Design",
            "ORM Basics",
            "Backups & Migrations",
        ],
    },
    {
        "title": "Web Development with Django",
        "description": "Build web apps with Django: models, views, templates and auth.",
        "lessons": [
            "Django project setup",
            "Models and Migrations",
            "Admin Customisation",
            "Views and URL routing",
            "Templates and static files",
            "Forms and validation",
            "Authentication & Permissions",
            "File uploads",
            "Testing Django apps",
            "Deployment basics",
        ],
    },
    {
        "title": "Operating Systems & Networking",
        "description": "Intro to OS concepts and fundamental networking principles.",
        "lessons": [
            "Processes and Threads",
            "Memory Management",
            "File Systems",
            "I/O and Drivers",
            "Concurrency basics",
            "Networking models (OSI/TCP/IP)",
            "Sockets and TCP/UDP",
            "Network troubleshooting",
            "Security basics",
            "System monitoring",
        ],
    },
    {
        "title": "Software Engineering Practices",
        "description": "Design, testing and team practices for reliable software.",
        "lessons": [
            "Software development lifecycle",
            "Design patterns overview",
            "Modular design",
            "Unit testing",
            "Integration testing",
            "CI/CD basics",
            "Code review best practices",
            "Documentation",
            "Project management basics",
            "Maintenance and refactoring",
        ],
    },
    {
        "title": "Microeconomics",
        "description": "Foundations of microeconomics: consumers, firms and markets.",
        "lessons": [
            "Supply and Demand",
            "Elasticity",
            "Consumer Choice",
            "Production & Costs",
            "Perfect Competition",
            "Monopoly & Market Power",
            "Oligopoly basics",
            "Market Failures",
            "Externalities",
            "Public Policy & Regulation",
        ],
    },
    {
        "title": "Macroeconomics",
        "description": "Aggregate economy: GDP, inflation, unemployment and policy.",
        "lessons": [
            "Measuring the Economy (GDP)",
            "Unemployment & Labor Markets",
            "Inflation & Price Indexes",
            "Aggregate Demand & Supply",
            "Fiscal Policy",
            "Monetary Policy",
            "Economic Growth",
            "Business Cycles",
            "Open Economy / Exchange Rates",
            "Policy Tradeoffs",
        ],
    },
    {
        "title": "Intro to Econometrics",
        "description": "Basics of data analysis and causal inference in economics.",
        "lessons": [
            "Data types & sources",
            "Statistical foundations",
            "Simple linear regression",
            "Multiple regression",
            "Hypothesis testing",
            "Model specification",
            "Heteroskedasticity & remedies",
            "Instrumental variables (intro)",
            "Panel data basics",
            "Interpreting results",
        ],
    },
]

class Command(BaseCommand):
    help = "Seed 10 curated courses (CS + Economics) with 10 lessons each (100 lessons)."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete existing courses and lessons first")
        parser.add_argument("--use-faker-content", action="store_true", help="Use Faker for lesson content/descriptions")

    def handle(self, *args, **options):
        fake = Faker()
        use_faker_content = options["use_faker_content"]

        if options["clear"]:
            Lesson.objects.all().delete()
            Course.objects.all().delete()
            self.stdout.write("Cleared existing Course and Lesson data")

        with transaction.atomic():
            created_courses = 0
            for cdata in RELEVANT_COURSES[:10]:
                course = Course.objects.create(
                    title=cdata["title"],
                    description=(fake.paragraph(nb_sentences=2) if use_faker_content else cdata["description"]),
                )
                created_courses += 1
                for idx, lesson_title in enumerate(cdata["lessons"][:10], start=1):
                    Lesson.objects.create(
                        course=course,
                        title=lesson_title,
                        content=(fake.paragraph(nb_sentences=4) if use_faker_content else f"Lesson: {lesson_title}\n\n{cdata['title']} - detailed content."),
                        position=idx,
                        is_done=False,
                    )

        self.stdout.write(self.style.SUCCESS(f"Created {created_courses} courses and {created_courses * 10} lessons"))