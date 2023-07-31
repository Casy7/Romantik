from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
# Create your views here.


def base_context(request, **args):
    context = {}
    django_user = request.user

    context['title'] = 'none'
    context['header'] = 'none'
    context['error'] = 0
    context['is_superuser'] = False

    if args != None:
        for arg in args:
            context[arg] = args[arg]

    return context


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home')
        return render(request, "home.html", context)