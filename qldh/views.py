from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Username: "+request.POST.get('username') + " Password: "+request.POST.get('password'))
            if user_type == 1:
                return redirect('admin_home')
            elif user_type == 2:
                # return HttpResponse("Teacher Login")
                return redirect('teacher_home')
            elif user_type == 3:
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Bạn không có quyền đăng nhập!")
                return redirect('login')
        else:
            messages.error(request, "Thông tin đăng nhập không hợp lệ!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/qldh/')
