from students.models import StudentModule

def assign_modules_to_student(student, courses):
    """
    Automatically assign all modules of the selected courses to a student.
    """
    for course in courses:
        for module in course.modules.all():
            StudentModule.objects.get_or_create(
                student=student,
                module=module,
                defaults={'status': 'pending'}
            )
