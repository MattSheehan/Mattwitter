'''
COPYRIGHT Matt Sheehan 2021
'''
import random
from django.conf import settings  # settings module
from django.shortcuts import render, redirect  # navigation
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url  # safe url routing
from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>HttpResponse says hello!</h1>")
    return render(request, template_name="pages/Home.html", context={}, status=200)

# list http client methods for view to support
@api_view(['POST'])
def tweet_create_view(request, *args, **kwargs):
    '''
    Django Rest Framework API Create View
    -> converting forms to serializers
    -> notice how associations are passed into the objects
    '''
    serializer = TweetSerializer(data=request.POST or None)
    # raise_exception=True -> if error then send error msg
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    '''
    Django Rest Framework API List View
    '''
    query_set = Tweet.objects.all()
    serializer = TweetSerializer(query_set, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def mattweets_view(request, tweet_id, *args, **kwargs):
    '''
    REST API View
    consume by JavaScript -> returns JSON data
    '''
    query_set = Tweet.objects.filter(id=tweet_id)
    if not query_set.exists():
        # status 404 = not found
        return Response({}, status=404)
    obj = query_set.first()
    # pass single instance of object to serialize
    serializer = TweetSerializer(obj)
    # JsonResponse ≈ json.dumps
    return Response(serializer.data, status=200)


# Below is the RAW Django API views implementation without using the REST framework
# As we can see, using Django HTML Forms instead of serializers is tedious.
'''
def tweet_create_PURE_DJANGO_view(request, *args, **kwargs):
    # associate user to tweet request object
    user = request.user
    # check if user is authenticated
    if not request.user.is_authenticated:
        # user is not authenticated
        user = None
        if request.is_ajax():
            # 401 = unauthorized
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    # initialize TweetForm class with or without data.
    form = TweetForm(request.POST or None)
    # request.POST = Querry Dictionary
    next_url = request.POST.get("next") or None
    # if form is valid, else render the invalid form
    if form.is_valid():
        # save the form
        obj = form.save(commit=False)
        # user is authenticated
        obj.user = user
        # save form to the database
        obj.save()
        # true if request is XMLHttpRequest
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        # IMPORTANT: reinitialize a new blank form
        form = TweetForm()
    if form.errors:
        return JsonResponse(form.errors, status=400)
    # render form
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_PURE_DJANGO_view(request, *args, **kwargs):
    query_set = Tweet.objects.all()
    # dictionary list of data. serialize() gets instance of object in the models
    tweets_list = [x.serialize() for x in query_set]
    data = {
        "isUser": False,
        "response": tweets_list,
    }
    return JsonResponse(data)


# dynamic URL routing
def mattweets_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
        # "image_path": obj.image.url
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

'''
