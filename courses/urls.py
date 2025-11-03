from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/add/', views.add_course, name='add_course'),
    path('course/<int:pk>/enroll/', views.enroll_course, name='enroll'),
    path('course/<int:pk>/unenroll/', views.unenroll_course, name='unenroll'),
    path('course/<int:course_pk>/student/<int:student_pk>/edit-score/', views.edit_score, name='edit_score'),
]
