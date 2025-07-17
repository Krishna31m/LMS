from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quiz, Question, Option
from .models import VideoLesson #Course, CourseVideo


class RoleUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

# class QuizForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields = ['title', 'course', 'pdf']

class VideoLessonForm(forms.ModelForm):
    class Meta:
        model = VideoLesson
        fields = ['course', 'title', 'video_file', 'description', 'order']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']