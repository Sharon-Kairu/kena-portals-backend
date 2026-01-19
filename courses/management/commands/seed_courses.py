from django.core.management.base import BaseCommand
from courses.models import Course, Module

class Command(BaseCommand):
    help = "Seed initial courses and modules"

    def handle(self, *args, **kwargs):
        # Example: Computer course
        computer = Course.objects.get_or_create(name="Computer")[0]
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
            Module.objects.get_or_create(course=computer, title=title, order=i)
        
        ai=Course.objects.get_or_create(name='AI')[0]
        ai_modules=[
            "Introduction to Ai and its basics",
            "Prompt Engineering",
            "Image Generation",
            "Video Generation",
            "Research and writing Assistants",
            "AI models Overview"
        ]
        for i,title in enumerate(ai_modules, starts=1):
            Module.objects.get_or_create(course=ai, title=title)