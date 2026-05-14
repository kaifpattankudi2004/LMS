from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    path('ai-chat-response/', views.ai_chat_response, name='ai_chat_response'),
    
    # Notes URLs
    path('notes/', views.subject_list, name='subject_list'),
    path('notes/create-subject/', views.create_subject, name='create_subject'),
    path('notes/delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('notes/<int:subject_id>/', views.notes_list, name='notes_list'),
    path('notes/<int:subject_id>/create/', views.create_note, name='create_note'),
    path('notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),

]
