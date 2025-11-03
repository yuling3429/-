from django.db import models
from django.conf import settings


class Student(models.Model):
    name = models.CharField(max_length=100)
    # optional link to Django User for authentication
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    midterm_score = models.IntegerField(null=True, blank=True)
    final_score = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # For new enrollments, set default 0 scores if not provided (no randomness here).
        if self.pk is None:
            if self.midterm_score is None:
                self.midterm_score = 0
            if self.final_score is None:
                self.final_score = 0
        super().save(*args, **kwargs)

    @property
    def average_score(self):
        if self.midterm_score is not None and self.final_score is not None:
            return (self.midterm_score + self.final_score) / 2
        return None

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course}: {self.midterm_score}"
