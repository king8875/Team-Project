from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Question, Answer, Category, Expert_Category, Expert, Expert_answer, Pet
from django.utils import timezone
from django.http import HttpResponse
from .forms import QuestionForm , AnswerForm, ExpertForm, ExpertAnswerForm,PetForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializer import MovieSerializer
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.db.models import Q
from django.db.models import Count
from .models import Post, Photo, Events
import openai
from django.http import JsonResponse
import cv2
from django.core.files.storage import default_storage
from .models import Tanalyze
from django.core.files import File
from django.core.files.base import ContentFile
from .models import ForumQuestion
from .models import ForumAnswer

from .forms import ForumQuestionForm
from .forms import ForumAnswerForm
from .forms import ProfileImgForm



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = MovieSerializer

class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')
            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_rest_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력

def main(request, category_name='expert'):
    '''
    pybo 목록 출력
    '''
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    expert = Expert.objects.all()
    category_list = Expert_Category.objects.all()
    #print(category_list)
    category = get_object_or_404(Expert_Category, name=category_name)
    question_list = Expert.objects.filter(category=category)
    ###expert_list변경
    # 정렬
    if so == 'recommend':
        # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 질문 제목검색
            Q(content__icontains=kw) |  # 질문 내용검색
            Q(answer__content__icontains=kw) |  # 답변 내용검색
            Q(author__username__icontains=kw) |  # 질문 작성자검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list,3)  # 페이지당 10개식 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category, 'expert':expert}
    
    return render(request, 'pybo/main.html', context)






def index(request, category_name='qna'):
    '''
    pybo 목록 출력
    '''
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)

    # 정렬
    if so == 'recommend':
        # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 질문 제목검색
            Q(content__icontains=kw) |  # 질문 내용검색
            Q(answer__content__icontains=kw) |  # 답변 내용검색
            Q(author__username__icontains=kw) |  # 질문 작성자검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개식 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category}
    return render(request, 'pybo/question_list.html', context)
# Create your views here.

def index3(request, category_name='qna'):
    '''
    pybo 목록 출력
    '''
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)

    # 정렬
    if so == 'recommend':
        # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 질문 제목검색
            Q(content__icontains=kw) |  # 질문 내용검색
            Q(answer__content__icontains=kw) |  # 답변 내용검색
            Q(author__username__icontains=kw) |  # 질문 작성자검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개식 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category}
    return render(request, 'pybo/question_list.html', context)




def index2(request):
    openai.api_key = "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"

   
    if request.method == "POST":
        #prompt = input("알렉산더 : ")
        animal_species = request.POST.get('animal-species','')
        others = request.POST.get('others','')
        detailed_type = request.POST.get('detailed-type','')
        other_species = request.POST.get('other-species','')
        age = request.POST.get('age','')
        ages = request.POST.get('ages','')
        gpt1 = request.POST.get('gpt1','')
        prompt = "나이가 " + ages + "인 " + others + "의 " + other_species + "종이 " + str(gpt1)
        print(prompt)
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        #prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: Where is the Valley of Kings?\nA:",
        temperature=1,
        max_tokens=3700,
        #top_p=1,
        #frequency_penalty=0.0,
        #presence_penalty=0.0,
        #stop=["\n"]
        )
        context = {'question_list': response["choices"][0]["text"].strip()}
        
        
       
        return render(request, 'pybo/alexander_list.html',context)#, context)
        
    else:
        print("get")
        return render(request, 'pybo/alexander_list.html')#, context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    photo = Photo.objects.all()
    context = {'question': question, 'photo' : photo}
    return render(request, 'pybo/question_detail.html', context)

def expert_detail(request, question_id):
    question = get_object_or_404(Expert, pk=question_id)
    photo = Photo.objects.all()
    context = {'question': question, 'photo' : photo}
    return render(request, 'pybo/expert_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def expert_answer_create(request, question_id):
    question = get_object_or_404(Expert, pk=question_id)
    if request.method == "POST":
        form = ExpertAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            print(question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:expert_detail', question_id=question.id), answer.id))
    else:
        form = ExpertAnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/expert_detail.html', context)

@login_required(login_url='common:login')
def question_create(request, category_name):
    """
    pybo 질문등록
    """
    category = Category.objects.get(name=category_name)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.category = category
            question.save()
            #return redirect(category)
            
    else:  # request.method == 'GET'
        form = QuestionForm()
    context = {'form': form, 'category': category}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'category': question.category}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def expert_modify(request, question_id):
    question = get_object_or_404(Expert, pk=question_id)
    if request.user != question.author:
        print('hi')
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:expert_detail', question_id=question.id)
    if request.method == "POST":
        form = ExpertForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:expert_detail', question_id=question.id)
    else:
        form = ExpertForm(instance=question)
    context = {'form': form, 'category': question.category}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def expert_answer_modify(request, answer_id):
    answer = get_object_or_404(Expert_answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = ExpertAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:expert_detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def expert_delete(request, question_id):
    question = get_object_or_404(Expert, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:expert_detail', question_id=question.id)
    question.delete()
    return redirect('pybo:expert')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def expert_answer_delete(request, answer_id):
    answer = get_object_or_404(Expert_answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:expert_detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def expert_vote(request, expert_id):
    expert = get_object_or_404(Expert, pk=expert_id)
    if request.user == expert.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        expert.voter.add(request.user)
    return redirect('pybo:expert_detail', expert_id=expert.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))




@login_required(login_url='common:login')
def user_profile(request):
    return render(request, 'common/profile_base.html')

@login_required(login_url='common:login')
def user_question(request):
    question_list = Question.objects.order_by('-create_date')
    category = Category.objects.order_by('id')
    context = {'category': category, 'question_list': question_list}
    print(category)
    return render(request, 'common/profile_question.html', context)

@login_required(login_url='common:login')
def user_comment(request):
    return render(request, 'common/profile_comment.html')

@login_required(login_url='common:login')
def user_answer(request):
    question_list = Question.objects.order_by('-create_date')
    answer_list = Answer.objects.order_by('-create_date')
    category = Category.objects.order_by('id')
    context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, 'common/profile_answer.html', context)











def expert(request, category_name='expert'):
    '''
    pybo 목록 출력
    '''
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    expert = Expert.objects.all()
    category_list = Expert_Category.objects.all()
    #print(category_list)
    category = get_object_or_404(Expert_Category, name=category_name)
    question_list = Expert.objects.filter(category=category)
    ###expert_list변경
    # 정렬
    if so == 'recommend':
        # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 질문 제목검색
            Q(content__icontains=kw) |  # 질문 내용검색
            Q(answer__content__icontains=kw) |  # 답변 내용검색
            Q(author__username__icontains=kw) |  # 질문 작성자검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개식 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category, 'expert':expert}
    return render(request, 'pybo/expert_list.html', context)

@login_required(login_url='common:login')
def expert_create(request, category_name):
    """
    pybo 질문등록
    """
    category = Expert_Category.objects.get(name=category_name)
    print(category)
    expert = Expert.objects.all
    
    if request.method == 'POST':
        """post = Post()
        photo = Photo()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.pub_date = timezone.datetime.now()
        post.user = request.user
        photo.post = post
        photo.image = request.POST['imgs']
        
        post.save()
        photo.save()
        
        
       
        for img in request.FILES.getlist('imgs'):
            print('hi in img')
            # Photo 객체를 하나 생성한다.
            photo = Photo()
            # 외래키로 현재 생성한 Post의 기본키를 참조한다.
            photo.post = post
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.image = img
            # 데이터베이스에 저장
            print(type(photo))
            photo.save()"""
        
        form = ExpertForm(request.POST, request.FILES)
        if form.is_valid():
            expert = form.save(commit=False)
            expert.author = request.user  # author 속성에 로그인 계정 저장
            expert.create_date = timezone.now()
            expert.category = category  
           
            expert.save()
           
            #return redirect(category)
            #return redirect('pybo:expert_detail')
            #expert = get_object_or_404(Question, pk=expert_id)
            context = {'question': expert, 'form': form}
            return render(request, 'pybo/expert_detail.html',context)
        else:
            print(form.errors)
    else:  # request.method == 'GET'
        form = ExpertForm()
   
    context = {'form': form, 'category': category}
    return render(request, 'pybo/question_form.html', context)

def pet_create(request,question_id):
    pet = get_object_or_404(Pet, pk=question_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            #return redirect('pybo:pet_create')
            context = {'pet': pet}
            return render(request, 'pybo/pet_create.html', context)
    else:
        form = PetForm()
    return render(request, 'pybo/pet_create.html', {'form': form})



def randing_page(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, 'registration/randing.html')







# 1. Channel-Community

def createChannel(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '1.channelCommunity/create.html')

def listChannel(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '1.channelCommunity/list.html')

def medicalCaseChannel(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '1.channelCommunity/medicalCase.html')

def scheduleChannel(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '1.channelCommunity/schedule.html')


# 2. group

def createGroup(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '2.group/create.html')

@login_required(login_url='common:login')
def forumGroup(request):


    # questions = ForumQuestion.objects.all()

    questions = ForumQuestion.objects.all().order_by('-create_date')[:10]  # 최신순으로 정렬
    photo = Photo.objects.all()
    votor = ForumQuestion.objects.all().values_list('voter', flat=True)

    for question in questions:
        
        answers = ForumAnswer.objects.filter(question=question)
        question.answers = answers
    
    context = {'questions': questions, 'photo' : photo, 'votor' : votor}
    return render(request, '2.group/forum.html', context)


def listGroup(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '2.group/list.html')


# 3. board

def newsBoard(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '3.board/news.html')

def medicalInfoBoard(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '3.board/medicalInfo.html')

def etcBoard(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '3.board/etc.html')


# 4. chatgpt

def searchChatgpt(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '4.chatgpt/search.html')

def relatedInformationChatgpt(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '4.chatgpt/relatedInformation.html')

def etcChatgpt(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '4.chatgpt/etc.html')


# 5. registration

def publicUserRegistration(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '5.registration/publicUser.html')

def medicalUserRegistration(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '5.registration/medicalUser.html')

def etcRegistration(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '5.registration/etc.html')


# 6. ai-Check

def createDataAICheck(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '6.ai-Check/createData.html')

def createPHRAICheck(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '6.ai-Check/createPHR.html')

def etcAICheck(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '6.ai-Check/etc.html')


# 7. setting

def setting(request):
    #question_list = Question.objects.order_by('-create_date')
    #answer_list = Answer.objects.order_by('-create_date')
    #category = Category.objects.order_by('id')
    #context = {'category': category, 'question_list': question_list, 'answer_list' : answer_list}
    #print(category)
    return render(request, '7.setting/setting.html')

def dangbti(request):
    
    return render(request, 'pybo/mbti.html')

# def animalContest(request):
    
#     return render(request, 'pybo/animal_contest.html')

# def animalRanking(request):
    
#     return render(request, 'pybo/animal_ranking.html')

# def animalWrite(request):
    
#     return render(request, 'pybo/animal_write.html')









@login_required(login_url='common:login')
def calendar(request):  
    print('1')
    #category = Events.objects.order_by('id')
    author = request.user
    print(author)
    
    all_events = Events.objects.filter(author=author)
    print(all_events)
    #all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'pybo/calendar.html',context)
@login_required(login_url='common:login') 
def all_events(request):   
    print('2')
    author = request.user   
    print(author)                                                                                           
    all_events = Events.objects.filter(author=author)                                                                             
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False)                                                                                                              
                                                                                                                      
 
@login_required(login_url='common:login') 
def add_event(request):
    print('3')
    author = request.user
    print(author)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end, author = author)
    event.save()
    data = {}
    return JsonResponse(data)

@login_required(login_url='common:login') 
def update(request):
    print('4')
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
@login_required(login_url='common:login') 
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

# 환자 post views.py 코드
from django.shortcuts import render
from .models import PatientList, Tanalyze


def Tanalyze(request):
    tanalyze = Tanalyze.objects.all()
    context = {
        'tanalyze': tanalyze
    }
    return JsonResponse(context)




def patient_list(request):
    patients = PatientList.objects.all()
    context = {
        'patients': patients
    }
    return render(request, 'patient_list.html', context)


# 신규 환자 생성
from django.shortcuts import render, redirect
from .forms import PatientForm

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.author = request.user
            patient.save()
            return redirect('patient_list')  # 'patient_list'를 환자 목록 뷰의 URL 이름으로 바꾸세요
    else:
        form = PatientForm()
    return render(request, 'your_template.html', {'form': form})








def process_image_function(img):
    # 이미지 처리
    x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
    absX = cv2.convertScaleAbs(x)  # uint8로 변환
    absY = cv2.convertScaleAbs(y)
    result = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

    return result



def process_image(request):
    # Tanalyze 모델 인스턴스 가져오기
    tanalyze_instance = Tanalyze.objects.all()[1]  # 예시로 첫 번째 인스턴스를 가져옴

    # 이미지 파일 읽기
    image = tanalyze_instance.side_sephalo  
    # 이미지 파일 읽기
    img = cv2.imread(image.path)
    # 이미지 처리
    result = process_image_function(img)

    # 결과 이미지를 저장할 필드에 할당
    result_image = ContentFile(cv2.imencode('.jpg', result)[1].tostring())

    # Tanalyze 모델 인스턴스 업데이트
    tanalyze_instance.side_sephalo_line.save('result.jpg', result_image)
  
    # 결과 이미지의 URL을 변수에 할당
    result_image_url = tanalyze_instance.side_sephalo_line.url

    context = {'result_image_url': result_image_url}

    return render(request, '6.ai-Check/createData_line.html', context)

@login_required(login_url='common:login')
def create_forum_question(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        # forum_img = request.FILES.get('forum_img')  # 이미지 파일 가져오기

        forum_img = ForumQuestionForm(request.POST, request.FILES)
        # ForumQuestion 모델에 데이터 저장
        forum_question = ForumQuestion(
            author=request.user,
            subject=subject, 
            content=content,
            # forum_img=forum_img,
            modify_date=None,
            create_date=timezone.now(),
            category=None,
            )
        forum_question.save()
        context = {'forum_question': forum_question}
        return redirect('pybo:forumGroup')
    return render(request, '2.group/forum.html', context)



@login_required(login_url='common:login')
def forum_question_delete(request, question_id):
    question = get_object_or_404(ForumQuestion, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:forumGroup', question_id=question.id)
    question.delete()
    return redirect('pybo:forumGroup')



# @login_required(login_url='common:login')
# def create_forum_answer(request, answer_id):
#     if request.method == 'POST':
#         question = ForumAnswer.objects.get(pk=answer_id)
#         author = request.user
#         content = request.POST['content']
#         create_date = timezone.now()

#         answer = ForumAnswer(question=question, author=author, content=content, create_date=create_date)
#         answer.save()
        
#         return redirect('2.group/forum.html', answer_id=answer_id)
    

@login_required(login_url='common:login')
def create_forum_answer(request, question_id):
    question = get_object_or_404(ForumQuestion, pk=question_id)
    if request.method == "POST":
        form = ForumAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            print(question.id)
            return redirect('pybo:forumGroup')
    else:
        form = ForumAnswerForm()
    context = {'question': question, 'form': form}
    return render(request, '2.group/forum.html', context)


@login_required(login_url='common:login')
def forum_question_vote(request, question_id):
    question = get_object_or_404(ForumQuestion, pk=question_id)
    if request.user == question.author:
        messages.error(request, 'error')
    else:
        question.voter.add(request.user)
    return redirect('pybo:forumGroup', question_id=question.id)








@login_required(login_url='common:login')
def forum_answer_modify(request, answer_id):
    answer = get_object_or_404(ForumAnswer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:forumGroup', question_id=answer.question.id)
    if request.method == "POST":
        form = ForumAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:forumGroup')

    else:
        form = ForumAnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def forum_answer_delete(request, answer_id):
    answer = get_object_or_404(ForumAnswer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')

    else:
        answer.delete()
    return redirect('pybo:forumGroup', question_id=answer.question.id)

# @login_required(login_url='common:login')
# def answer_delete(request, answer_id):
#     answer = get_object_or_404(Answer, pk=answer_id)
#     if request.user != answer.author:
#         messages.error(request, '삭제권한이 없습니다')
#     else:
#         answer.delete()
#     return redirect('pybo:detail', question_id=answer.question.id)
    





@login_required(login_url='common:login')

def forum(request):
    if request.method == 'POST':
        form = ForumQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('forum')
    else:
        form = ForumQuestionForm()
    questions = ForumQuestion.objects.all()
    context = {'questions': questions}
    return render(request, '2.group/forum.html', context)



def fetch_more_posts(request):
    last_question_id = request.GET.get('last_question_id')  # 마지막으로 로드한 질문의 ID를 가져옴

    # 마지막으로 로드한 질문 ID보다 작은 ID를 가진 질문들을 가져옴
    questions = ForumQuestion.objects.filter(id__lt=last_question_id).order_by('-create_date')[:10]

    # 질문들을 JSON 형식으로 직렬화하여 응답
    data = {
        'questions': [
            {
                'id': question.id,
                'subject': question.subject,
                'content': question.content,
                'author': question.author.username,
                'create_date': question.create_date.isoformat(),
            }
            for question in questions
        ]
    }
    return render(request, '2.group/forum.html', data)


def upload_profile_img(request):
    if request.method == 'POST':
        form = ProfileImgForm(request.POST, request.FILES)
        if form.is_valid():
            profile_img = form.save(commit=False)
            profile_img.author = request.user
            profile_img.save()
            return redirect('pybo/user_profile.html')
    else:
        form = ProfileImgForm()
    return render(request, 'pybo/user_profile.html', {'form': form})




from .models import animal_ranking
from .models import animal_ranking_Category
from .forms import animalForm


def animalContest(request,category_name='animal_ranking'):
    
    '''
    pybo 목록 출력
    '''
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    animal = animal_ranking.objects.all()
    category_list = animal_ranking_Category.objects.all()
    #print(category_list)
    category = get_object_or_404(animal_ranking_Category, name=category_name)
    question_list = animal_ranking.objects.filter(category=category)
    ###expert_list변경
    # 정렬
    if so == 'recommend':
        # aggretation, annotation에는 relationship에 대한 역방향 참조도 가능 (ex. Count('voter'))
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 질문 제목검색
            Q(content__icontains=kw) |  # 질문 내용검색
            Q(answer__content__icontains=kw) |  # 답변 내용검색
            Q(author__username__icontains=kw) |  # 질문 작성자검색
            Q(answer__author__username__icontains=kw)  # 답변 작성자검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 9)  # 페이지당 10개식 보여주기
    page_obj = paginator.get_page(page)
    max_index = len(paginator.page_range)

    context = {'question_list': page_obj, 'max_index': max_index, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list, 'category': category, 'animal':animal}
    return render(request, 'pybo/animal_contest.html', context)


@login_required(login_url='common:login')
def animalWrite(request,category_name='animal_ranking'):
    """
    pybo 질문등록
    """
    category = animal_ranking_Category.objects.get(name=category_name)
    print(category)
    aniaml = animal_ranking.objects.all
    form = animalForm(request.POST, request.FILES)
    if request.method == 'POST':
        """post = Post()
        photo = Photo()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.pub_date = timezone.datetime.now()
        post.user = request.user
        photo.post = post
        photo.image = request.POST['imgs']
        
        post.save()
        photo.save()
        
        
       
        for img in request.FILES.getlist('imgs'):
            print('hi in img')
            # Photo 객체를 하나 생성한다.
            photo = Photo()
            # 외래키로 현재 생성한 Post의 기본키를 참조한다.
            photo.post = post
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.image = img
            # 데이터베이스에 저장
            print(type(photo))
            photo.save()"""
        
        form = animalForm(request.POST, request.FILES)
        if form.is_valid():
            aniaml = form.save(commit=False)
            aniaml.author = request.user  # author 속성에 로그인 계정 저장
            aniaml.create_date = timezone.now()
            aniaml.category = category  
           
            aniaml.save()
           
            #return redirect(category)
            #return redirect('pybo:expert_detail')
            #expert = get_object_or_404(Question, pk=expert_id)
            context = {'aniaml': aniaml, 'form': form}
            print("123123")
            return redirect('pybo:animalcontest', category_name='animal_ranking')
        else:
            print(form.errors)
    else:  # request.method == 'GET'
        form = animalForm()
        print("gdgd")
    context = {'form': form, 'category': category}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def animal_vote(request, question_id):
    question = get_object_or_404(animal_ranking, pk=question_id)
    
    question.voter.add(request.user)
    return redirect('pybo:animalcontest', category_name='animal_ranking')