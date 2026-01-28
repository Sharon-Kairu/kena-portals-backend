from django.core.management.base import BaseCommand
from courses.models import Course, SubscriptionPlan

class Command(BaseCommand):
    help = "Seed initial subscription plans with courses"

    def handle(self, *args, **kwargs):
        # Get all courses
        all_courses = list(Course.objects.all())

        # Define plans
        plans = {
            "bronze": all_courses[:1],      # e.g., first course only
            "gold": all_courses[:2],        # first two courses
            "platinum": all_courses         # all courses
        }

        for plan_name, courses in plans.items():
            plan, created = SubscriptionPlan.objects.get_or_create(name=plan_name)
            plan.included_courses.set(courses)  # Assign courses to plan
            plan.save()

        self.stdout.write(self.style.SUCCESS("Subscription plans seeded successfully"))
