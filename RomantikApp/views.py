import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser

from .models import NewsPost
# Create your views here.


def full_name(user):
    if user.last_name != '' and user.first_name != '':
        return user.first_name+' '+user.last_name
    elif user.first_name != '':
        return user.first_name
    elif user.last_name != '':
        return user.last_name
    else:
        return user.username
    

def base_context(request, **args):
    context = {}
    django_user = request.user

    context['title'] = 'none'
    context['user'] = 'none'
    context['header'] = 'none'
    context['error'] = 0
    context['is_superuser'] = False

    if len(User.objects.filter(username=django_user.username)) != 0 and type(request.user) != AnonymousUser:

        user = User.objects.get(username=django_user.username)
        context['username'] = django_user.username
        context['full_name'] = full_name(user)
        context['user'] = user

        if request.user.is_superuser:
            context['is_superuser'] = True

    if args != None:
        for arg in args:
            context[arg] = args[arg]

    return context


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home')
        return render(request, "home.html", context)


class NewsPage(View):
    def get(self, request):

        context = base_context(request, title='Новини', header='Новини')
        context['news'] = sorted(NewsPost.objects.all(), key=lambda obj: obj.datetime)
        context['news'].reverse()
        return render(request, "news.html", context)


class AjaxPublishPost(View, LoginRequiredMixin):
    def post(self, request):
        form = request.POST

        news_post = NewsPost(
            user=request.user,
            datetime=datetime.datetime.now(),   
            content=form['news_content'],     
            img_paths="" 
        )
        news_post.save()

        result = {}
        result["result"] = "success"
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class Login(View):

    def __init__(self):
        self.error = 0

    def get(self, request):

        context = base_context(
            request, title='Вхід', header='Вхід', error=0)
        context['error'] = 0

        # context['form'] = self.form_class()
        return render(request, "signin.html", context)

    def post(self, request):
        context = {}
        form = request.POST

        username = form['username']
        password = form['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                context['name'] = username
                return HttpResponseRedirect("/")

        else:
            context = base_context(request, title='Вхід', header='Вхід')
            logout(request)
            context['error'] = 1
            # return Posts.get(self,request)
            return render(request, "signin.html", context)


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class SignUp(View):
    def get(self, request):

        context = base_context(
            request, title='Реєстрація', header='Реєстрація', error=0)

        return render(request, "signup.html", context)

    def post(self, request):
        context = {}
        form = request.POST
        user_props = {}
        username = form['username']
        password = form['password']

        # new_post.author = Author.objects.get(id = request.POST.author)
        # new_post.save()
        user = User.objects.filter(username=username)
        if list(user) == []:
            for prop in form:
                if prop not in ('csrfmiddlewaretoken', 'username', 'gender', 'phone_number') and form[prop] != '':
                    user_props[prop] = form[prop]

            auth_user = User.objects.create_user(username=form['username'], **user_props)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")

        else:
            context = base_context(request, title='Реєстрація', header='Реєстрація')

            for field_name in form.keys():
                context[field_name] = form[field_name]

            context['error'] = 1
            return render(request, "signup.html", context)
