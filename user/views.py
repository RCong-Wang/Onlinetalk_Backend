# ****這邊沒有使用viewsets

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

from .forms import FormLogin, CustomUserCreationForm
from .models import UserProfile
from .serializers import UserProfileSerializer
# Create your views here.
def get_csrf_token(request):
    csrf = get_token(request)
    return JsonResponse({'csrf_token':csrf})
# def get_csrf_token(request):
#     # Your view logic here
#     response = JsonResponse({'message': 'Your response message'})
    
#     # Set the CSRF token as a cookie
#     response.set_cookie('csrftoken', get_token(request), httponly=True, samesite='Strict')

#     return response

def check_user_login(request):
    if request.user.is_authenticated:
        return JsonResponse({'loggin': True})
    else:
        return JsonResponse({'loggin': False})

def userlogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({'success': True})
            response.set_cookie('sessionid', request.session.session_key, httponly=True)
            return response
        else:
            return JsonResponse({'success':False},status=401)

@login_required
def userlogout(request):
    logout(request)
    return JsonResponse({'success':True})

def usersignin(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/login/')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'user/signin.html', context)

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_userprofile(sender, instance, **kwargs):
    instance.userprofile.save()





from django.http import HttpResponse

@login_required
def add_friend(request):
    user_a_profile = request.user.userprofile
    friend_id = int(request.body)
    user_b = get_object_or_404(UserProfile,id=friend_id)
    user_a_profile.friend.add(user_b)
    user_a_profile.save()

    return JsonResponse({'success': 'successful add'})


def search_friend(request):
    if request.method == "GET":
        username = request.GET.get('username')
        users = User.objects.get(username=username)
        if not users:
            return JsonResponse({'success: ':"Not username"})
        else:
            context = {'user':users.username,'user_id':users.userprofile.id}
            return JsonResponse(context)

@login_required
def friend_list(request):
    friends = request.user.userprofile.friend.all()
    # serializer = UserProfileSerializer(user_profile)
    # serialized_data = serializer.data
    friend_list = []
    for friend in friends:
        friend_data = {'friend_name':friend.user.username,'friend_id':friend.id}
        friend_list.append(friend_data)
    context = {'friends': friend_list}
    return JsonResponse(context)





