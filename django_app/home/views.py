from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.result import AsyncResult
from .task import analyse_repo_task


@api_view(['POST'])
def begin_task(request):
    data = request.data
    repo_url = data.get('repo_url')
    pr_num = data.get("pr_num")
    git_token = data.get('git_token')
    task = analyse_repo_task.delay(repo_url,pr_num,git_token)

    return Response({
        "task_id": task.id,
        "status": "Task Started",
    })


@api_view(['GET'])
def task_status_view(request,task_id):
    
    result = AsyncResult(task_id)
    response = {
        "task_id" : task_id,
        "status" : result.state,
        "result" : result.result
    }
    return Response(response)
 