from django.core.management.base import BaseCommand

from courses.models import Student, Teacher, Course, Enrollment


class Command(BaseCommand):
    help = 'Populate sample data: one student and three courses with enrollments and midterm scores.'

    def handle(self, *args, **options):
        # create a student (you)
        student, _ = Student.objects.get_or_create(name='莊閎翔')

        # create a teacher
        teacher, _ = Teacher.objects.get_or_create(name='王老師')

        # create three courses
        courses_info = [
            ('程式設計', 'CS101', 85),
            ('資料庫系統', 'CS102', 78),
            ('作業系統', 'CS103', 92),
        ]

        for name, code, score in courses_info:
            course, _ = Course.objects.get_or_create(name=name, code=code, teacher=teacher)
            Enrollment.objects.update_or_create(student=student, course=course, defaults={'midterm_score': score})

        self.stdout.write(self.style.SUCCESS('Sample data created: student and 3 courses with scores.'))
