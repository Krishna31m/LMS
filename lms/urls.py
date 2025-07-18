from django.urls import path
from . import views
# from .views import update_profile
from .views import RegisterView, LoginView, LogoutView, StudentDashboardView, TeacherDashboardView, AddQuestionView, AttemptQuizView, CourseListView, EditQuizTitleView, EditQuizQuestionsView, DeleteQuizView
from .views import CreateCourseView, UpdateCourseView, DeleteCourseView, EnrollCourseView, UploadQuizView, QuizListView, CourseDetailView, AssignmentCreateView,AssignmentEditView, AssignmentListView, AssignmentDeleteView, AssignmentViewView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dashboards
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    # path('student/dashboard/', student_dashboard, name='student_dashboard'),


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

    # 
    path('quiz/<int:quiz_id>/edit/', EditQuizTitleView.as_view(), name='edit_quiz_title'),
    path('quiz/<int:quiz_id>/edit-questions/', EditQuizQuestionsView.as_view(), name='edit_quiz_questions'),
    path('quiz/<int:quiz_id>/delete/', DeleteQuizView.as_view(), name='delete_quiz'),

    # Assignment
    path('assignments/', AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:assignment_id>/edit/', AssignmentEditView.as_view(), name='assignment_edit'),
    path('assignments/<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('assignments/<int:pk>/view/', AssignmentViewView.as_view(), name='assignment_view'),

    # path('update-profile/', update_profile, name='update_profile'),
]
