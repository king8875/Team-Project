from django.contrib import admin

from .models import Question, Post, Photo, Expert, Pet, Profile_img, animal_ranking_Category, ForumQuestion, animal_ranking


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
admin.site.register(animal_ranking)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Post, PostAdmin)
# Register your models here.
