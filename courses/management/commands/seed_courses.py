from django.core.management.base import BaseCommand
from courses.models import Course, Module,CourseCategory

class Command(BaseCommand):
    help = "Seed initial courses and modules"

    def handle(self, *args, **kwargs):
        # COMPUTER COURSE
        computer, _ = Course.objects.get_or_create(name="computer")
        computer_modules = [
            "Introduction to computers",
            "Computer Systems and hardware",
            "MS Windows",
            "MS Word",
            "MS Excel",
            "MS Access",
            "MS Publisher",
            "PowerPoint",
            "Email and Internet",
            "Computer Maintenance"
        ]

        for i, title in enumerate(computer_modules, start=1):
            Module.objects.get_or_create(
                course=computer,
                title=title,
                order=i
            )

        # AI COURSE
        ai, _ = Course.objects.get_or_create(name="ai")
        ai_modules = [
            "Introduction to AI and its basics",
            "Prompt Engineering",
            "Image Generation",
            "Video Generation",
            "Research and Writing Assistants",
            "AI Models Overview"
        ]

        for i, title in enumerate(ai_modules, start=1):
            Module.objects.get_or_create(
                course=ai,
                title=title,
                order=i
            )

        driving, _ = Course.objects.get_or_create(name="driving")
        driving, _ = Course.objects.get_or_create(name="driving")
        
        # Create categories using choice values
        practical, _ = CourseCategory.objects.get_or_create(
            course=driving,
            name='practical',  # Use the choice value
            defaults={'order': 1}
        )
        
        theory, _ = CourseCategory.objects.get_or_create(
            course=driving,
            name='theory',  # Use the choice value
            defaults={'order': 2}
        )
        driving_modiles=[
            "Introduction",
            "Use of break,clutch and handbrake",
            "Changing Gears",
            "Steering Control",
            "Road Positioning",
            "Turning Right and Left",
            "Use of Mirrors and hand signals",
            "Reverse PT1",
            "Parking PT1(ANGLE AND FLASH)",
            "Driving Assessment 1",
            "Changing Lanes",
            "Acceleration and Overtaking",
            "Roundabouts",
            "U TURN",
            "Reverse PT2",
            "Parking PT2 (ANGLE AND FLASH)",
            "Theory Board Assessment",
            "Driving Assessment 2",
            "Basic Mechanical",
            "Junction Drill",
            "Three Point Turn",
            "Examination Evaluation Test",
            "Hill Start",
            "Parking PT3(ANGLE AND FLASH)",
            "Reversing PT3"
        ]
        for i, title, in enumerate(driving_modiles, start=1):
            Module.objects.get_or_create(
                course=driving,
                title=title,
                order=i
            )

        self.stdout.write(self.style.SUCCESS("Courses and modules seeded successfully"))
