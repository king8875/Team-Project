from django.contrib import admin
<<<<<<< HEAD
from .models import Question, Post, Photo, Expert, Pet, Profile_img, animal_ranking_Category
=======
from .models import Question, Post, Photo, Expert, Pet, Profile_img, ForumQuestion
>>>>>>> 1d4887f7b7de7b9ed9535a0b1ac5c928d510ab97

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

class PhotoInline(admin.TabularInline):
    model = Photo

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]


admin.site.register(Pet)
admin.site.register(Expert)
admin.site.register(ForumQuestion)


admin.site.register(Profile_img)

admin.site.register(animal_ranking_Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Post, PostAdmin)
# Register your models here.
