from django.shortcuts import render
from django.views.decorators.http import require_POST
import json
from .models import *
from django.http import JsonResponse

@require_POST
def update_task_status_ajax(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status in ['Backlog','To Do','In Progress','Completed']:
            task.status = new_status
            task.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False,'error':'Invalid status'},status=400)
    except Task.DoesNotExist:
        return JsonResponse({'success':False,'error':'Task not found'},status=404)
