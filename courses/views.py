from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Student, Teacher, Enrollment
from django.db.models import Avg
from django.db import IntegrityError
from .forms import CourseForm, ScoreForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    # Determine current student: prefer authenticated user's linked Student, fallback to first Student
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student
        except Exception:
            student = None
    if not student:
        student = Student.objects.first()

    if student:
        enrollments = student.enrollment_set.select_related('course', 'course__teacher')
        courses = [e.course for e in enrollments]
    else:
        courses = []

    # Compute per-course data including student's enrollment and class average of averages
    course_data = []
    for course in courses:
        # student's enrollment for this course
        student_enrollment = course.enrollments.filter(student=student).first() if student else None

        # class average (average of each student's average_score)
        all_enrollments = course.enrollments.all()
        valid_averages = [e.average_score for e in all_enrollments if e.average_score is not None]
        class_avg = (sum(valid_averages) / len(valid_averages)) if valid_averages else None

        course_data.append({
            'course': course,
            'student_enrollment': student_enrollment,
            'class_avg': class_avg,
        })

    return render(request, 'courses/index.html', {'course_data': course_data, 'student': student})


def course_detail(request, pk):
    course = get_object_or_404(Course.objects.select_related('teacher').prefetch_related('enrollments__student'), pk=pk)
    enrollments = course.enrollments.select_related('student')
    # current student logic
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student
        except Exception:
            student = None
    if not student:
        student = Student.objects.first()
    is_enrolled = False
    if student:
        is_enrolled = course.enrollments.filter(student=student).exists()
    return render(request, 'courses/course_detail.html', {'course': course, 'enrollments': enrollments, 'student': student, 'is_enrolled': is_enrolled})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            teacher = form.cleaned_data.get('teacher')
            new_teacher_name = form.cleaned_data.get('new_teacher')
            # If a new teacher name is provided, create/use it and prefer it over dropdown
            if new_teacher_name:
                teacher, _ = Teacher.objects.get_or_create(name=new_teacher_name)
            # If neither provided, set teacher to None (but Course requires teacher) — rely on form input; here we guard
            if not teacher:
                # fallback: try to get any teacher or create a placeholder
                teacher, _ = Teacher.objects.get_or_create(name='未命名老師')
            # Use code as the primary uniqueness key and handle race conditions
            try:
                # If a course with this code already exists, inform the user
                course = Course.objects.get(code=code)
                messages.info(request, f'課程「{course.name}」已存在')
            except Course.DoesNotExist:
                try:
                    course = Course.objects.create(name=name, code=code, teacher=teacher)
                    messages.success(request, f'課程「{course.name}」已建立')
                    # Auto-enroll all existing students with random scores
                    from .models import Enrollment
                    import random
                    for student_obj in Student.objects.all():
                        Enrollment.objects.get_or_create(
                            student=student_obj,
                            course=course,
                            defaults={
                                'midterm_score': random.randint(0, 100),
                                'final_score': random.randint(0, 100),
                            }
                        )
                except IntegrityError:
                    # Handle a rare race where another request created the same code concurrently
                    course = Course.objects.get(code=code)
                    messages.info(request, f'課程「{course.name}」已存在')
            # redirect to the newly created / existing course detail
            return redirect('courses:course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})


@login_required
@require_POST
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # determine student (prefer logged-in user's linked Student)
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student
        except Exception:
            student = None
    if not student:
        student = Student.objects.first()
    if not student:
        return redirect('courses:index')
    Enrollment.objects.get_or_create(student=student, course=course)
    messages.success(request, f'已為 {student.name} 加選 {course.name}')
    return redirect('courses:course_detail', pk=pk)


@login_required
@require_POST
def unenroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    student = None
    if request.user.is_authenticated:
        try:
            student = request.user.student
        except Exception:
            student = None
    if not student:
        student = Student.objects.first()
    if not student:
        return redirect('courses:index')
    Enrollment.objects.filter(student=student, course=course).delete()
    messages.success(request, f'已為 {student.name} 退選 {course.name}')
    return redirect('courses:course_detail', pk=pk)


@login_required
def edit_score(request, course_pk, student_pk):
    enrollment = get_object_or_404(
        Enrollment,
        course_id=course_pk,
        student_id=student_pk
    )
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, f'成績已更新')
            return redirect('courses:course_detail', pk=course_pk)
    else:
        form = ScoreForm(instance=enrollment)
    
    context = {
        'form': form,
        'enrollment': enrollment,
        'course': enrollment.course,
        'student': enrollment.student
    }
    return render(request, 'courses/edit_score.html', context)
