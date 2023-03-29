from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .todo_model import Todo
import json

def http_wrapper(function):
    
    def wrapper(request, **kwargs):
        body = json.loads(request.body) if request.body else {}
        method = request.method
        headers = request.headers
        try:
            return function(body=body, method=method, headers=headers, params=kwargs)
        except Exception as error:
            print(error)
            return JsonResponse(status=500, data={ "message": str(error) }, safe=False)

    
    return wrapper

@csrf_exempt
@http_wrapper
def todo_controller(**kwargs):
    method = kwargs['method']
    def get_handler(**kwargs):
        return JsonResponse(list(Todo.objects.all().values()), safe=False)

    def post_handler(**kwargs):
        body = kwargs['body']
        Todo(
            title=body['title']
        ).save()
        return HttpResponse(status=201)

    def update_handler(**kwargs):
        params, body = kwargs['params'], kwargs['body']
        if("title" in body):
            Todo.objects.filter(id=params['id']).update(title=body['title'])
        elif("isComplete" in body):
            Todo.objects.filter(id=params['id']).update(isComplete=body['isComplete'])
        else:
            return JsonResponse(status=500, data={"message": "No necessary parameters: id, isComplete"})
        todo = Todo.objects.filter(id=params['id']).values()
        return JsonResponse(status=202, data=list(todo), safe=False)
    
    def delete_handler(**kwargs):
        params = kwargs['params']
        Todo.objects.filter(id=params['id']).delete()
        return HttpResponse(status=204)
    
    handler = {
        "GET": get_handler,
        "POST": post_handler,
        "PUT": update_handler,
        "DELETE": delete_handler
    }
    
    if(method not in handler):
        return HttpResponse(status=404)

    return handler[method](**kwargs)
    
    


