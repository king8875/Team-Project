from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def __str__(self):
        return self.description

   

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.name])

class Question(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')
    def __str__(self):
        return self.subject


class Answer(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')




class Expert_Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def __str__(self):
        return self.description

   

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.name])

class Pet(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True)
    

class Expert(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert_author')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_expert')  # 추천인 추가
    category = models.ForeignKey(Expert_Category, on_delete=models.CASCADE, related_name='expert_category')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, related_name='pet')
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    def __str__(self):
        return self.subject
    
class Expert_answer(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expert_author_answer')
    question = models.ForeignKey(Expert, on_delete=models.CASCADE,related_name = 'expert_answers')
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='expert_voter_answer')
    def __str__(self):
        return self.content
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.title

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class Fullcalender(models.Model):
    #user_id = models.CharField(max_length=200)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Fullcalender_author')
    reservation_title = models.CharField(max_length=200)
    reservation_detail = models.CharField(max_length=200)
    reservation_date = models.DateTimeField()
    reservation_time = models.CharField(max_length=200)
    reservation_idx = models.IntegerField(null=True)


class Event(models.Model):
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

class Calendar(models.Model):
    #id = models.AutoField(primary_key=True)
    events = models.ManyToManyField(Event)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    
    def __str__(self):
        return f"{self.year}-{self.month}-{self.day}"
    
class animal_ranking_Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.name])
    
class Pet2(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True)

class animal_ranking(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animal_ranking_author')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_animal_ranking')  # 추천인 추가
    category = models.ForeignKey(animal_ranking_Category, on_delete=models.CASCADE, related_name='animal_ranking_category')
    pet = models.ForeignKey(Pet2, on_delete=models.CASCADE, null=True, related_name='pet2')
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    voter = models.ManyToManyField(User, related_name='voter_animal_question')
    
    def __str__(self):
        return self.subject





# Create your models here.
