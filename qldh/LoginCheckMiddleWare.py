from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        # if modulename == 'home.views':
        #     return redirect("home")
        # Check whether the user is logged in or not

        if user.is_authenticated:
            if user.user_type == 1:
                if modulename == "qldh.AdminView":
                    pass
                elif modulename == "qldh.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("QLDH:admin_home")

            elif user.user_type == 2:
                if modulename == "qldh.TeacherView":
                    pass
                elif modulename == "qldh.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("QLDH:teacher_home")

            elif user.user_type == 3:
                if modulename == "qldh.StudentView":
                    pass
                elif modulename == "qldh.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("QLDH:student_home")

            else:
                # if modulename == 'home.views':
                #     pass
                # else:
                return redirect("QLDH:login")

        else:
            if request.path == reverse("QLDH:login") or request.path == reverse("QLDH:doLogin"):
                pass
            else:
                if modulename == "home.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("home_page")
