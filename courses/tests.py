from django.test import TestCase, Client
from django.urls import reverse
from courses.models import Student, Teacher, Course, Enrollment
from django.contrib.auth.models import User


class EnrollmentTests(TestCase):
    def setUp(self):
        # create a user and student linked
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.student, _ = Student.objects.get_or_create(user=self.user, defaults={'name': 'Test Student'})
        self.teacher = Teacher.objects.create(name='T-Teach')
        self.course = Course.objects.create(name='Test Course', code='T100', teacher=self.teacher)
        self.client = Client()

    def test_enroll_and_unenroll(self):
        # login
        self.client.login(username='tester', password='testpass')

        enroll_url = reverse('courses:enroll', args=[self.course.pk])
        resp = self.client.post(enroll_url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

        unenroll_url = reverse('courses:unenroll', args=[self.course.pk])
        resp = self.client.post(unenroll_url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_signal_creates_student_and_login_required(self):
        # creating a new user should auto-create a Student via signal
        u = User.objects.create_user(username='signaluser', password='pw')
        self.assertTrue(Student.objects.filter(user=u).exists())

        # ensure add/enroll/unenroll require login
        self.client.logout()
        add_url = reverse('courses:add_course')
        resp = self.client.get(add_url)
        self.assertEqual(resp.status_code, 302)

        enroll_url = reverse('courses:enroll', args=[self.course.pk])
        resp = self.client.post(enroll_url)
        self.assertEqual(resp.status_code, 302)
