from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment, Progress, Subject, Note
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.http import JsonResponse
from openai import OpenAI
import os
import json

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        courses = Course.objects.all()
    return render(request, 'courses/home.html', {'courses': courses, 'query': query})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f"You have successfully enrolled in {course.title}")
    return redirect('course_detail', course_id=course.id)

@login_required
def lesson_detail(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You must be enrolled to view this lesson.")
        return redirect('course_detail', course_id=course.id)
    
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    
    if request.method == 'POST' and 'complete' in request.POST:
        progress.completed = True
        progress.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        messages.success(request, "Lesson marked as completed!")
        return redirect('lesson_detail', course_id=course.id, lesson_id=lesson.id)


    lessons = course.lessons.all().order_by('order')
    next_lesson = lessons.filter(order__gt=lesson.order).first()
    prev_lesson = lessons.filter(order__lt=lesson.order).last()

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'lessons': lessons,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson
    })

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    course_progress = []
    
    for enrollment in enrollments:
        total_lessons = enrollment.course.lessons.count()
        completed_lessons = Progress.objects.filter(
            user=request.user, 
            lesson__course=enrollment.course, 
            completed=True
        ).count()
        
        progress_percent = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        course_progress.append({
            'course': enrollment.course,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': round(progress_percent, 1)
        })
        
    return render(request, 'courses/dashboard.html', {'course_progress': course_progress})

@login_required
def ai_chat(request):
    return render(request, 'courses/ai_chat.html')

@login_required
def ai_chat_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            hf_token = os.environ.get('HF_TOKEN')
            if not hf_token:
                return JsonResponse({'error': 'AI Token not configured'}, status=500)

            client = OpenAI(
                base_url="https://router.huggingface.co/v1",
                api_key=hf_token,
            )

            completion = client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=[
                    {"role": "system", "content": "You are EduCore AI, a helpful learning assistant for an LMS."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
            )
            
            ai_response = completion.choices[0].message.content
            return JsonResponse({'response': ai_response})
            
        except Exception as e:
            return JsonResponse({'error': f'AI Error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def subject_list(request):
    subjects = Subject.objects.filter(user=request.user).annotate(note_count=Count('notes'))
    return render(request, 'notes/subjects.html', {'subjects': subjects})

@login_required
def create_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Subject.objects.create(user=request.user, name=name)
            messages.success(request, f"Subject '{name}' created successfully.")
        return redirect('subject_list')
    return redirect('subject_list')

@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.delete()
    messages.success(request, "Subject deleted successfully.")
    return redirect('subject_list')

@login_required
def notes_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    notes = subject.notes.all().order_by('-updated_at')
    # For the sidebar
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'notes/notes_list.html', {'subject': subject, 'notes': notes, 'subjects': subjects})

@login_required
def create_note(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Note.objects.create(user=request.user, subject=subject, title=title, content=content)
            messages.success(request, "Note created successfully.")
            return redirect('notes_list', subject_id=subject.id)
    return render(request, 'notes/note_form.html', {'subject': subject})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        messages.success(request, "Note updated successfully.")
        return redirect('notes_list', subject_id=note.subject.id)
    return render(request, 'notes/note_form.html', {'note': note, 'subject': note.subject})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    subject_id = note.subject.id
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect('notes_list', subject_id=subject_id)

