from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Student, Teacher, Course

class Command(BaseCommand):
    help = '建立測試資料'

    def handle(self, *args, **kwargs):
        # 確保有一個超級用戶
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('創建超級用戶 "admin"...')
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        
        # 創建或獲取學生
        admin_user = User.objects.get(username='admin')
        student, created = Student.objects.get_or_create(
            user=admin_user,
            defaults={'name': '測試學生'}
        )
        if created:
            self.stdout.write(f'創建學生記錄: {student.name}')
        
        # 創建測試老師
        teacher, created = Teacher.objects.get_or_create(
            name='測試老師'
        )
        if created:
            self.stdout.write(f'創建老師記錄: {teacher.name}')
        
        # 創建測試課程
        course, created = Course.objects.get_or_create(
            code='TEST101',
            defaults={
                'name': '測試課程',
                'teacher': teacher
            }
        )
        if created:
            self.stdout.write(f'創建課程記錄: {course.name}')
        
        self.stdout.write('完成！')