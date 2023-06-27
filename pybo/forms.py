from django import forms
from pybo.models import Question, Answer, Expert, Expert_answer, Pet
from django.db import connection
from .models import ForumQuestion
from .models import ForumAnswer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }  

class ExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        connection.close()
        fields = ['subject', 'content','thumbnail']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': '줴목',
            'content': '내용',
            'thumbnail': '썸네일',
        } 
        enctype = 'multipart/form-data'
    def __init__(self, *args, **kwargs):
        super(ExpertForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].required = False


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class ExpertAnswerForm(forms.ModelForm):
    class Meta:
        model = Expert_answer
        fields = ['content']
        labels = {
            'content': '뒙변내용',
        }

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['photo']

class ForumQuestionForm(forms.ModelForm):
    class Meta:
        model = ForumQuestion
        fields = ['subject', 'content', 'category','forumimg']

class ForumAnswerForm(forms.ModelForm):
    class Meta:
        model = ForumAnswer
        fields = ['content']
        labels = {
            'content': '뒙변내용',
        }
        from django import forms
from .models import PatientList

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientList
        fields = ['name', 'gender', 'birthday', 'progress', 'tag']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '성별'}),
            'birthday': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '생년월일'}),
            'progress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '진행 상태'}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '태그'}),
        }