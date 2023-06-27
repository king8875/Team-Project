from django.urls import path
from pybo.views import MovieViewSet
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include, re_path
app_name = 'pybo'

urlpatterns = [
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change-password/',auth_views.PasswordChangeView.as_view()),    
    path('answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),
    path('question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
    path('expert/vote/<int:expert_id>/', views.expert_vote, name='expert_vote'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('expert/answer/delete/<int:answer_id>/', views.expert_answer_delete, name='expert_answer_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('expert/modify/<int:question_id>/', views.expert_modify, name='expert_modify'),
    path('expert/answer/modify/<int:answer_id>/', views.expert_answer_modify, name='expert_answer_modify'),
    path('expert/question/delete/<int:question_id>/', views.expert_delete, name='expert_delete'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('index/', views.index, name='index'),
    path('', views.main, name='main'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('expert/answer/create/<int:question_id>/', views.expert_answer_create, name='expert_answer_create'),
    #path('question/create/', views.question_create, name='question_create'),
    path('profile/base/', views.user_profile, name='user_profile'),
    path('profile/question/', views.user_question, name='user_question'),
    path('profile/answer/', views.user_answer, name='user_answer'),
    path('profile/comment/', views.user_comment, name='user_comment'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('alexander/', views.index2, name='index2'),
    path('question/craete/<str:category_name>/', views.question_create, name='question_create'),
    path('question/list/', views.index, name='index'),
    path('question/list/<str:category_name>/', views.index, name='index'),
    path('question/detail/<int:question_id>/', views.detail, name='detail'),
    path('expert/detail/<int:question_id>/', views.expert_detail, name='expert_detail'),
    path('expert/', views.expert, name='expert'),
    path('expert/craete/<str:category_name>/', views.expert_create, name='expert_create'),
    path('create/<int:question_id>', views.pet_create, name='pet_create'),
    path('dangbti/', views.dangbti, name='dangbti'),
    path('animal/contest/', views.animalContest, name='animal_contest'),
    path('animal/ranking/', views.animalRanking, name='animal_ranking'),
    path('animal/write/', views.animalWrite, name='animal_write'),
    path('registration/randing/', views.randing_page, name='randing_page'),

    
    

    # 1. Channel-Community
    path('channelCommunity/create/', views.createChannel, name='createChannel'),
    path('channelCommunity/list/', views.listChannel, name='listChannel'),
    path('channelCommunity/medicalCase/', views.medicalCaseChannel, name='medicalCaseChannel'),
    path('channelCommunity/schedule/', views.scheduleChannel, name='scheduleChannel'),


    # 2. group
    path('group/create/', views.createGroup, name='createGroup'),
    path('group/list/', views.listGroup, name='listGroup'),
    path('group/forum/', views.forumGroup, name='forumGroup'),


    # 3. board
    path('board/news/', views.newsBoard, name='newsBoard'),
    path('board/medicalInfo/', views.medicalInfoBoard, name='medicalInfoBoard'),
    path('board/etc/', views.etcBoard, name='etcBoard'),


    # 4. board
    path('chatgpt/search/', views.searchChatgpt, name='searchChatgpt'),
    path('chatgpt/relatedInformation/', views.relatedInformationChatgpt, name='relatedInformationChatgpt'),
    path('chatgpt/etc/', views.etcChatgpt, name='etcChatgpt'),


    # 5. registration
    path('registration/publicUser/', views.publicUserRegistration, name='publicUserRegistration'),
    path('registragion/medicalUser/', views.medicalUserRegistration, name='medicalUserRegistration'),
    path('registration/etc/', views.etcRegistration, name='etcRegistration'),


    # 6. ai-Check
    path('aiCheck/createData/', views.createDataAICheck, name='createDataAICheck'),
    path('aiCheck/createPHR/', views.createPHRAICheck, name='createPHRAICheck'),
    path('aiCheck/etc/', views.etcAICheck, name='etcAICheck'),


    # 7. setting
    path('setting/', views.setting, name='setting'),


    path('cal/',views.calendar, name='calendar'),
    path('all_events/',views.all_events, name='all_events'),
    path('add_event/',views.add_event, name='add_event'),
    path('update/',views.update, name='update'),


]

