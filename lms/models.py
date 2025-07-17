from django.db import models
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=100)
    learners = models.PositiveIntegerField(default=0)
    original_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('published', 'Published'), ('draft', 'Draft'), ('pending', 'Pending')), default='draft')

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # prevents double enrollment

    def __str__(self):
        return f"{self.student.username} joined {self.course.title}"
    

# class Quiz(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     pdf = models.FileField(upload_to='quizzes/')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.course.title}"
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
    
class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)


class QuizListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            # Teacher: show quizzes related to teacher's courses
            courses = Course.objects.filter(teacher=request.user)
            quizzes = Quiz.objects.filter(course__in=courses)
        else:
            # Student: show quizzes related to enrolled courses
            enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course', flat=True)
            quizzes = Quiz.objects.filter(course__in=enrolled_courses)

        return render(request, 'lms/quiz_list.html', {'quizzes': quizzes})

class VideoLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)  # For sorting playlist

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']  # ensures ascending order in query

    def __str__(self):
        return f"{self.course.title} - {self.title}"