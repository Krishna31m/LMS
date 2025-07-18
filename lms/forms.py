from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quiz, Question, Option, Assignment
from .models import VideoLesson #Course, CourseVideo
from django import forms
# from .models import Profile


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


#Assignment



class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'uploaded_file', 'file_link']
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'placeholder': 'YYYY-MM-DD'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uploaded_file'].required = False




# class ProfileImageForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']
