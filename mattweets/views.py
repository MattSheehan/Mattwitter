# COPYRIGHT Matt Sheehan 2020
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
# URL routing
def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>HttpResponse says hello!</h1>")
    return render(request, template_name="pages/Home.html", context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    '''
    REST API View
    consume by JavaScript 
    return JSON data
    '''
    query_set = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content} for x in query_set]
    data = {
        "response": tweets_list,
    }
    return JsonResponse(data)

# dynamic URL routing
def mattweets_view(request, tweet_id, *args, **kwargs):
    '''
    REST API View
    consume by JavaScript 
    return JSON data
    '''
    data = {
        "id": tweet_id,
        #"image_path": obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "404: Tweet Not Found"
        status = 404

    # JsonResponse ≈ json.dumps
    return JsonResponse(data, status=status)

