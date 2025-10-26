from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
import json
from .forms import *
from .models import *
from django.http import JsonResponse
from project_app.models import *
from notifications.tasks import *

@require_POST
def update_task_status_ajax(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)
        new_status = data.get('status').title()
        if new_status in ['Backlog','To Do','In Progress','Completed']:
            task.status = new_status
            task.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False,'error':'Invalid status'},status=400)
    except Task.DoesNotExist:
        return JsonResponse({'success':False,'error':'Task not found'},status=404)
    
@require_POST
def create_task_ajax(request):
    name = request.POST.get('name')
    project_id = request.POST.get('project_id')
    user = request.user
    
    if not name:
        return JsonResponse({'success':False,'error':'Task title is required'})
    if not project_id:
        return JsonResponse({'success':False,'error':'Project id is required'})
    
    try:
        project = Project.objects.get(id=project_id)
        # create new task
        new_task = Task.objects.create(name=name,project=project,owner=user)
        return JsonResponse({'success':True,'task_id':new_task.id})
    except Project.DoesNotExist:
        return JsonResponse({'success':False,'error':'Project not found'})
    
def get_task(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'error':'Task not found'},status=404)
    
    if request.method == 'GET':
        task_data = {
            'task_id':task.id,
            'name':task.name,
            'description':task.description,
            'priority':task.priority,
            'start_date': task.start_date.isoformat() if task.start_date else '',
            'due_date': task.due_date.isoformat() if task.due_date else '',
        }
        return JsonResponse({'task_data':task_data})

def update_task(request,task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'success':True,
                                 'updatedTask': {
                                'id':task.id,
                                'name':task.name,
                                'description':task.description,
                                'priority':task.priority,
                                'start_date': task.start_date.isoformat() if task.start_date else '',
                                'due_date': task.due_date.isoformat() if task.due_date else '',
                            }
                                 })
        else:
            return JsonResponse({'success':False,'error':form.errors})
    return JsonResponse({'success':False,'error':'invalid request method'},status=405)

def assign_user_to_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskAssignForm(request.POST, instance=task)
        if form.is_valid():
            task=form.save()
            # send notification to user
            actor_username = request.user.username
            task_user_profile = task.task_assigned_to.profile
            verb = f'Dear {task_user_profile.full_name}, {task.name} assigned to you. Kindly finish as soon as possible...'
            object_id = task.id
            create_notification.delay(actor_username=actor_username, verb=verb,  object_id=object_id, content_type_model='task', content_type_app_label='tasks')
            return JsonResponse({
                'success':True,
                'user':{
                'id':task.task_assigned_to.id,
                'name':task.task_assigned_to.profile.full_name,
                'profile_picture_url':task.task_assigned_to.profile.profile_picture_url
                }
                })
    else:
        return JsonResponse({'success':False,'error':'Invalid request method...'},status=405)
    
def get_task_assign_form(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
        form = TaskAssignForm(initial={
            'task_id':task.id,
            'task_assigned_to':task.task_assigned_to.id if task.task_assigned_to else None
            })
        html = render_to_string('tasks/task_assign_form.html',{'form':form,'task':task},request=request)
        return JsonResponse({'html':html})
    except Task.DoesNotExist:
        return JsonResponse({'error':'Task not found'},status=405)