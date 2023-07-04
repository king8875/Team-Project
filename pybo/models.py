from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Profile_img(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_img_author')
    Profile_img = models.ImageField(upload_to='photos/',null=True,blank=True) 
    def __str__(self):
        return self.author


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



class Events(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_author')
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 
    class Meta:  
        db_table = "tblevents"

class Tanalyze(models.Model):        
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Tanalyze_author')
    side_sephalo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    side_sephalo_line = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    front_sephalo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    panorama = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    Front_face_photo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    smiley_face_photo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    degree_45_face_photo = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)  
    Side_face_picture = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    premises_on_the_right = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    premises_on_the_front = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 
    premises_on_the_left = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    occlusal_surface_of_the_maxilla = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    occlusal_surface_of_the_mandible = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    add_extra1 = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    add_extra2 = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    add_extra3 = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    add_extra4 = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    add_extra5 = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)
    add_extra6 = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True)

    #def __str__(self):
        #return self.subject

class PatientList(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='PatientList_author')
    idx = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    gender = models.CharField(max_length=255,null=True,blank=True)
    birthday = models.CharField(max_length=255,null=True,blank=True)
    progress = models.CharField(max_length=255,null=True,blank=True)
    tag = models.CharField(max_length=255,null=True,blank=True)
    icon = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.author

class ForumQuestion(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Forum_author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='Forum_voter_question')  # 추천인 추가
    category = models.ForeignKey(Category,null=True, on_delete=models.CASCADE, related_name='Forum_category_question')
    forumimg = models.ImageField(upload_to='photos/%Y/%m/%d/',null=True,blank=True) 

    def __str__(self):
        return self.subject


class ForumAnswer(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Forum_author_answer')
    question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='Forum_voter_answer')

# Create your models here.


# Create your models here.
