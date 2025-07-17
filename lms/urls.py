from django.urls import path
from . import views
from .views import RegisterView, LoginView, LogoutView, StudentDashboardView, TeacherDashboardView, AddQuestionView, AttemptQuizView, CourseListView
from .views import CreateCourseView, UpdateCourseView, DeleteCourseView, EnrollCourseView, UploadQuizView, QuizListView, CourseDetailView #UploadCourseVideoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dashboards
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),


    path('teacher/create-course/', CreateCourseView.as_view(), name='create_course'),
    path('teacher/edit-course/<int:pk>/', UpdateCourseView.as_view(), name='edit_course'),
    path('teacher/delete-course/<int:pk>/', DeleteCourseView.as_view(), name='delete_course'),
    # path('student/enroll/<int:course_id>/', EnrollCourseView.as_view(), name='enroll_course'),

    # Quiz
    path('teacher/upload-quiz/', UploadQuizView.as_view(), name='upload_quiz'),
    path('student/quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('upload-quiz/', UploadQuizView.as_view(), name='upload_quiz'),
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('attempt-quiz/<int:quiz_id>/', AttemptQuizView.as_view(), name='attempt_quiz'),


    path('upload-quiz/', UploadQuizView.as_view(), name='upload_quiz'),
    path('quiz/<int:quiz_id>/add-question/', AddQuestionView.as_view(), name='add_question'),
    path('quiz/<int:quiz_id>/attempt/', AttemptQuizView.as_view(), name='attempt_quiz'),


    # video
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/upload_video/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('video/<int:video_id>/delete/', views.delete_video, name='delete_video'),

    # course
    path('student/enroll/<int:course_id>/', EnrollCourseView.as_view(), name='enroll_course'),
    path('courses/', CourseListView.as_view(), name='course_list'),

    path('enroll/<int:course_id>/', EnrollCourseView.as_view(), name='enroll_course'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),

    
]
