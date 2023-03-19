from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from .forms import *


# Create your views here.
def index(request):
    return render(request, 'portfolio/index.html', {
        'title': 'Main',
    })


def my_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "<strong>경고!</strong> 로그인이 필요한 작업입니다. ", extra_tags="alert-danger")
        return redirect('login')

    # 유저의 기본 정보를 불러옵니다.
    user_info = User.objects.get(pk=request.user.pk)
    user_profile = Profile.objects.get(pk=request.user.pk)
    # 유저가 가입한 서비스의 정보를 불러옵니다. 정보가 없을 경우를 대비하여 filter()를 사용합니다.
    user_career = Career.objects.filter(pk=request.user.pk).first()

    return render(request, 'registration/profile.html', {
        'title': '내 프로필',
        'user_info': user_info,
        'user_profile': user_profile,
        'user_career': user_career,
    })


def profile(request, username):
    # 유저의 기본 정보를 불러옵니다.
    user_info = User.objects.get(username=username)
    user_profile = Profile.objects.get(pk=user_info.pk)
    # 유저가 가입한 서비스의 정보를 불러옵니다. 정보가 없을 경우를 대비하여 filter()를 사용합니다.
    user_career = Career.objects.filter(pk=user_info.pk).first()

    return render(request, 'registration/profile.html', {
        'title': '{}님의 프로필'.format(user_info.username),
        'user_info': user_info,
        'user_profile': user_profile,
        'user_career': user_career,
    })


def register(request):
    if request.method == "POST":
        form_user = RegisterForm(request.POST)
        form_profile = ProfileRegisterForm(request.POST)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            messages.success(request, "<strong>성공!</strong> 회원가입에 성공하였습니다. 로그인하여 주십시오.", extra_tags="alert-success")
            return redirect('login')
        else:
            messages.warning(request, str(form_user.errors) + str(form_profile.errors), extra_tags="alert-danger")
            return redirect('register')

    else:
        form_user = RegisterForm()
        form_profile = ProfileRegisterForm()
        return render(request, 'registration/register.html', {'form_user': form_user, 'form_profile': form_profile})


def edit_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "<strong>경고!</strong> 로그인이 필요한 작업입니다. ", extra_tags="alert-danger")
        return redirect('login')

    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk)
        profile = Profile.objects.get(pk=request.user.pk)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']

        profile.birthday = request.POST['birthday']

        user.save()
        profile.save()
        return redirect('my_profile')
    # 유저의 기본 정보를 불러옵니다.
    user_info = User.objects.get(pk=request.user.pk)
    user_profile = Profile.objects.get(pk=request.user.pk)
    return render(request, 'registration/edit_profile.html', {
        'title': '프로필 수정',
        'user_info': user_info,
        'user_profile': user_profile,
    })


def projects(request):
    return render(request, 'portfolio/projects.html', {
        'title': '프로젝트',
    })


def lab(request):
    return render(request, 'portfolio/laboratory.html', {
        'title': '실험실',
    })
