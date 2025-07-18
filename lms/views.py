from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from .forms import ProfileImageForm
from django import forms 
from django.views.generic import CreateView, DeleteView, DetailView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import (
    RoleUserCreationForm, QuizForm, QuestionForm, OptionForm,
    VideoLessonForm, AssignmentForm
)
from .models import Course, Quiz, Enrollment, VideoLesson, Option, QuizAttempt, Assignment

from collections import Counter


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('student_dashboard') if not request.user.is_staff else redirect('teacher_dashboard')
        form = RoleUserCreationForm()
        return render(request, 'lms/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('student_dashboard') if not request.user.is_staff else redirect('teacher_dashboard')
        form = RoleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')

            # Teacher gets is_staff True, student gets False
            user.is_staff = True if role == 'teacher' else False
            user.save()
            login(request, user)

            # Redirect after login
            if user.is_staff:
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

        return render(request, 'lms/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('teacher_dashboard') if request.user.is_staff else redirect('student_dashboard')
        form = AuthenticationForm()
        return render(request, 'lms/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('teacher_dashboard') if request.user.is_staff else redirect('student_dashboard')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on role
            return redirect('teacher_dashboard') if user.is_staff else redirect('student_dashboard')

        return render(request, 'lms/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
        return render(request, 'lms/student_dashboard.html', {
            'enrollments': enrollments
        })
# Profile student 
# def student_dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')

#     profile = request.user.profile
#     enrollments = Enrollment.objects.filter(user=request.user)

#     if request.method == 'POST':
#         form = ProfileImageForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('student_dashboard')
#     else:
#         form = ProfileImageForm(instance=profile)

#     return render(request, 'lms/student_dashboard.html', {
#         'enrollments': enrollments,
#         'form': form,
#     })





class TeacherDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('student_dashboard')

        courses = Course.objects.filter(teacher=request.user)

        course_counts = {
            'published': courses.filter(status='published').count(),
            'pending': courses.filter(status='pending').count(),
            'draft': courses.filter(status='draft').count(),
        }

        # Get all enrollments for teacher’s courses
        enrollments_by_course = {}
        for course in courses:
            enrollments = Enrollment.objects.filter(course=course).select_related('student')
            enrollments_by_course[course.id] = enrollments

        context = {
            'courses': courses,
            'course_counts': course_counts,
            'enrollments_by_course': enrollments_by_course,
        }
        return render(request, 'lms/teacher_dashboard.html', context)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'thumbnail', 'description', 'duration', 'original_price', 'discount_price', 'status']

class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'lms/create_course.html'
    success_url = reverse_lazy('teacher_dashboard')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)
    


class UpdateCourseView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'lms/create_course.html'  # reuse the form
    success_url = reverse_lazy('teacher_dashboard')

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class DeleteCourseView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'lms/confirm_delete.html'
    success_url = reverse_lazy('teacher_dashboard')

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)  # secure
    

class EnrollCourseView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        if request.user.is_staff:
            messages.error(request, "Only students can enroll.")
            return redirect('teacher_dashboard')

        course = Course.objects.get(id=course_id)

        # Prevent duplicate
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )

        if created:
            messages.success(request, f'Enrolled in {course.title}')
        else:
            messages.info(request, 'You are already enrolled.')

        return redirect('student_dashboard')
    

# class UploadQuizView(LoginRequiredMixin, View):
#     def get(self, request):
#         if not request.user.is_staff:
#             return redirect('student_dashboard')

#         form = QuizForm()
#         form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
#         return render(request, 'lms/upload_quiz.html', {'form': form})

#     def post(self, request):
#         if not request.user.is_staff:
#             return redirect('student_dashboard')

#         form = QuizForm(request.POST, request.FILES)
#         form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('teacher_dashboard')
#         return render(request, 'lms/upload_quiz.html', {'form': form})
class UploadQuizView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('student_dashboard')
        form = QuizForm()
        form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
        return render(request, 'lms/upload_quiz.html', {'form': form})

    def post(self, request):
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('add_question', quiz_id=quiz.id)
        return render(request, 'lms/upload_quiz.html', {'form': form})


from django.shortcuts import get_object_or_404

class AddQuestionView(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        question_form = QuestionForm()
        return render(request, 'lms/add_question.html', {
            'question_form': question_form,
            'quiz': quiz
        })

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        question_form = QuestionForm(request.POST)
        
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            for i in range(1, 5):
                text = request.POST.get(f'option{i}')
                correct = request.POST.get('correct') == str(i)
                Option.objects.create(question=question, option_text=text, is_correct=correct)

            return redirect('add_question', quiz_id=quiz.id)

        return render(request, 'lms/add_question.html', {
            'question_form': question_form,
            'quiz': quiz
        })


class AttemptQuizView(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.question_set.all()
        return render(request, 'lms/attempt_quiz.html', {'quiz': quiz, 'questions': questions})

    def post(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.question_set.all()
        score = 0

        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                option = Option.objects.get(id=selected_option_id)
                if option.is_correct:
                    score += 1

        QuizAttempt.objects.create(student=request.user, quiz=quiz, score=score)
        return render(request, 'lms/quiz_result.html', {'score': score, 'total': questions.count()})


class QuizListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            # Teacher view: Show their uploaded quizzes
            quizzes = Quiz.objects.filter(course__teacher=request.user)
        else:
            # Student view: Show quizzes for enrolled courses
            enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
            quizzes = Quiz.objects.filter(course__in=enrolled_courses)
        return render(request, 'lms/quiz_list.html', {'quizzes': quizzes})

class EditQuizTitleView(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        form = QuizForm(instance=quiz)
        return render(request, 'lms/edit_quiz_title.html', {'form': form, 'quiz': quiz})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('edit_quiz_questions', quiz_id=quiz.id)
        return render(request, 'lms/edit_quiz_title.html', {'form': form, 'quiz': quiz})

class EditQuizQuestionsView(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.question_set.all()
        return render(request, 'lms/quiz_question_edit.html', {'quiz': quiz, 'questions': questions})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.question_set.all()

        for question in questions:
            question_text = request.POST.get(f'question_{question.id}')
            if question_text:
                question.question_text = question_text
                question.save()

            for option in question.option_set.all():
                option_text = request.POST.get(f'option_{option.id}')
                is_correct = f'correct_{question.id}' in request.POST and request.POST[f'correct_{question.id}'] == str(option.id)
                option.option_text = option_text
                option.is_correct = is_correct
                option.save()

        return redirect('quiz_list')

class DeleteQuizView(LoginRequiredMixin, View):
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.delete()
        return redirect('quiz_list')




def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = VideoLesson.objects.filter(course=course).order_by('order')
    return render(request, 'lms/course_detail.html', {'course': course, 'videos': videos})

def upload_video(request, course_id):
    if not request.user.is_staff:
        raise PermissionDenied("Only teachers can upload videos.")

    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = VideoLessonForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = VideoLessonForm()

    return render(request, 'lms/upload_video.html', {'form': form, 'course': course})

def edit_video(request, video_id):
    video = get_object_or_404(VideoLesson, id=video_id)

    if not request.user.is_staff or video.course.teacher != request.user:
        raise PermissionDenied("Only the course teacher can edit this video.")

    form = VideoLessonForm(request.POST or None, request.FILES or None, instance=video)
    if form.is_valid():
        form.save()
        return redirect('course_detail', course_id=video.course.id)
    return render(request, 'lms/edit_video.html', {'form': form})


def delete_video(request, video_id):
    video = get_object_or_404(VideoLesson, id=video_id)

    if not request.user.is_staff or video.course.teacher != request.user:
        raise PermissionDenied("Only the course teacher can delete this video.")

    course_id = video.course.id
    video.delete()
    return redirect('course_detail', course_id=course_id)



class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # Staff (teachers) can access their course
        if request.user.is_staff and course.teacher == request.user:
            pass  # allow

        # Students can only access if enrolled
        elif not request.user.is_staff:
            is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
            if not is_enrolled:
                messages.error(request, "You are not enrolled in this course.")
                return redirect('student_dashboard')

        # Fetch and show videos
        videos = VideoLesson.objects.filter(course=course).order_by('order')
        return render(request, 'lms/course_detail.html', {'course': course, 'videos': videos})




class CourseListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            return redirect('teacher_dashboard')  # Only for students

        # Show all available courses with an enroll button
        enrolled = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        courses = Course.objects.exclude(id__in=enrolled)
        return render(request, 'lms/student_courses.html', {'courses': courses})
    


# Assignment

class AssignmentListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            courses = Course.objects.filter(teacher=request.user)
            assignments = Assignment.objects.filter(course__in=courses)
        else:
            enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
            assignments = Assignment.objects.filter(course__in=enrolled_courses)

        return render(request, 'lms/assignment_list.html', {'assignments': assignments})

class AssignmentCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('student_dashboard')
        form = AssignmentForm()
        form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
        return render(request, 'lms/assignment_create.html', {'form': form})

    def post(self, request):
        if not request.user.is_staff:
            return redirect('student_dashboard')
        form = AssignmentForm(request.POST, request.FILES)  # ✅ handle uploaded files
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
        return render(request, 'lms/assignment_create.html', {'form': form})

class AssignmentEditView(LoginRequiredMixin, View):
    def get(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        if not request.user.is_staff or assignment.course.teacher != request.user:
            return redirect('assignment_list')
        form = AssignmentForm(instance=assignment)
        form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
        return render(request, 'lms/assignment_edit.html', {'form': form, 'assignment': assignment})

    def post(self, request, assignment_id):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        if not request.user.is_staff or assignment.course.teacher != request.user:
            return redirect('assignment_list')
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)  # ✅ handle uploaded files
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
        return render(request, 'lms/assignment_edit.html', {'form': form, 'assignment': assignment})


class AssignmentDeleteView(DeleteView):
    model = Assignment
    template_name = 'lms/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignment_list')

    def get_queryset(self):
        return Assignment.objects.filter(course__teacher=self.request.user)
    
class AssignmentViewView(DetailView):
    model = Assignment
    template_name = 'assignments/view_assignment.html'
    context_object_name = 'assignment'


# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         profile = request.user.profile
#         if 'profile_image' in request.FILES:
#             profile.image = request.FILES['profile_image']
#             profile.save()
#         return redirect('student_dashboard')  # redirect after saving
    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()