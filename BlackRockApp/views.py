import json
import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser


from django.views.generic import View, TemplateView
from django import forms
from json import loads
from BlackRockApp.code.classes import NewEquipment

from BlackRockProject.settings import BASE_DIR, DATABASE_PWD
from .models import *
from datetime import date, timedelta, datetime


from .code.db_connect import *
import psycopg


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
    context['header'] = 'none'
    context['error'] = 0
    context['is_superuser'] = False

    if args != None:
        for arg in args:
            context[arg] = args[arg]


    if len(Users.objects.filter(username=django_user.username)) != 0 and type(request.user) != AnonymousUser:

        user = Users.objects.get(username=django_user.username)
        context['username'] = django_user.username
        context['full_name'] = full_name(user)
        context['user'] = user

        if request.user.is_superuser:
            context['is_superuser'] = True

    else:
        context['avatar'] = ''
        context['username'] = 'Adminius'
        context['user'] = 'none'

    return context


def get_all_contacts():
    contacts = []
    for contact in Users.objects.all():
        contacts.append((contact.id, contact.name, contact.phone_number))
    return contacts


def beauty_date_interval(date1: datetime, date2: datetime, show_year=False, show_if_this_year=False):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    result = ''
    result += str(date1.day) + ' '

    if (date1.day, date1.month, date1.year) == (date2.day, date2.month, date2.year):
        result += months[date1.month-1]
    else:
        if date1.month == date2.month:
            result += '- '+str(date2.day) + ' ' + months[date1.month-1]
        else:
            result += months[date1.month-1]+' - ' + \
                str(date2.day) + ' '+months[date2.month-1]

    if show_year:
        if show_if_this_year:
            result += ', '+str(date1.year)
        else:
            if date1.year != datetime.now().year:
                result += ', '+str(date1.year)

    return result


def get_cathegory_path(cathegory):
    cathegory_path = cathegory.name
    curr_cathegory = cathegory
    while curr_cathegory.parent_cathegory != None:
        curr_cathegory = curr_cathegory.parent_cathegory
        cathegory_path = curr_cathegory.name + '/' + cathegory_path
    return cathegory_path


def get_all_free_equipment():
    eq_list = []
    for equipment in Equipment.objects.all():
        eq_list.append((equipment.id,
                        equipment.name,
                        get_cathegory_path(equipment.cathegory),
                        equipment.description,
                        float(equipment.price),
                        int(equipment.amount)))
        # TODO Append filters to filter only free equipment
    return eq_list


class HomePage(View):
    def get(self, request):
        context = base_context(request, title='Home')
        return render(request, "home.html", context)
    

class Registration(View):
    def get(self, request):

        context = base_context(
            request, title='Sign Up', header='Sign Up', error=0)

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

            # print(user_props)
            auth_user = User.objects.create_user(
                username=form['username'], **user_props)
            
            
            custom_user = Users(
                username =form['username'],
                first_name = form['first_name'],
                last_name = form['last_name'],
                email = form['email'],
                phone_number = form['phone_number'],
                confidence_factor = 0,
                profile_approved = False)
            

            with psycopg.connect("host=127.0.0.1 port=5432 dbname=rentequipmentservicedb user=django password="+DATABASE_PWD) as conn:
                with conn.cursor() as cur:
                    resp = cur.execute("""CREATE USER """+form['username']+""" PASSWORD '"""+auth_user.password+"""' IN ROLE single_user """)
                    print(resp)
                    pass


            
            custom_user.save()

            user = authenticate(username=username, password=password)
            login(request, user)

            # print(form)
            return HttpResponseRedirect("/")

        else:
            context = base_context(request, title='Sign Up',
                                   header='Sign Up')

            for field_name in form.keys():
                context[field_name] = form[field_name]

            context['error'] = 1
            return render(request, "signup.html", context)
    

class Login(View):

    def __init__(self):
        self.error = 0

    def get(self, request):

        context = base_context(
            request, title='Sign In', header='Sign In', error=0)
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
            context = base_context(request, title='Sign In', header='Sign In')
            logout(request)
            context['error'] = 1
            # return Posts.get(self,request)
            return render(request, "signin.html", context)


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class CreateUser(View):
    def get(self, request):
        context = base_context(
            request, title='Новый контакт', header='Добавить нового пользователя')
        return render(request, "add_contact.html", context)

    def post(self, request):

        form = request.POST

        name_input = form['name_input']
        number_input = form['number_input']
        in_club_input = form['in_club_input'] == "on"

        contact = Contact(
            name=name_input,
            phone_number=number_input,
            is_club_member=in_club_input,
        )

        contact.save()

        return HttpResponseRedirect("/new_contact")


class AddEquipment(View, LoginRequiredMixin):
    def get(self, request):

        if request.user.is_anonymous:
            return HttpResponseRedirect("/")
        
        if request.user.is_superuser:
            
            context = base_context(
                request, title='Add an equipment', header='Add an equipment')
            eq_list = get_all_free_equipment()
            context['eq_list'] = eq_list
            # context['contacts_list'] = contacts_list
            return render(request, "add_equpment.html", context)
        
        else:
            return HttpResponseRedirect("/")


class CreateNewRentAccounting(View, LoginRequiredMixin):
    def get(self, request):

        if request.user.is_anonymous:
            return HttpResponseRedirect("/signin")
        
        context = base_context(
            request, title='Арендовать снаряжение', header='Арендовать снаряжение')
        eq_list = get_all_free_equipment()
        context['eq_list'] = eq_list
        return render(request, "new_rent_accounting.html", context)
            

    def post(self, request):

        if request.user.is_anonymous:
            return HttpResponseRedirect("/")

        form = request.POST

        username = request.user.username
        password = request.user.password
        db_connection = DBConnection(username, password)

        db_connection.create_accounting(form['start_date'], form['end_date'])

        equipment_json = loads(form['equipmentJSON'])

        for eqId in equipment_json:
            equipment = Equipment.objects.get(id=eqId)
            if equipment_json[eqId] == 1:                
                db_connection.add_equipment_to_accounting(eqId)
            else:
                db_connection.add_countable_equipment_to_accounting(eqId, equipment_json[eqId])

        return HttpResponseRedirect("/")


class MyRentAccountings(View, LoginRequiredMixin):
    def get(self, request):
        context = base_context(request, title='Your rent accountings', header='Записи аренды')
        
        username = request.user.username
        password = request.user.password
        db_connection = DBConnection(username, password)
        accountings = db_connection.get_all_user_accountings()

        context['accountings'] = accountings
        
        return render(request, "my_rent_accountings.html", context)


class AddNewEquipment(View, LoginRequiredMixin):

    def post(self, request):
        req = request
        form = request.POST

        result = {}
        result["result"] = "failture"

        username = request.user.username
        password = request.user.password
        db_connection = DBConnection(username, password)

        if form["requestType"] == "add":
            try:
                new_equipment = NewEquipment(form['obj[name]'], form['obj[path]'], form['obj[desc]'], form['obj[price]'], form['obj[amount]'])
                new_equipment_id = db_connection.create_new_equipment(new_equipment)

                result['new_id'] = new_equipment_id
                result["result"] = "success"
            except:
                result["result"] = "failture"

        elif form["requestType"] == "update":
            try:
                equipment_id = int(form['obj[id]'])
                updated_equipment = NewEquipment(form['obj[name]'], form['obj[path]'], form['obj[desc]'], form['obj[price]'], form['obj[amount]'])

                db_connection.update_equipment(equipment_id, updated_equipment)
                result["result"] = "success"
            except:
                result["result"] = "failture"
        
        elif form["requestType"] == "remove":
            try:
                equipment_id = int(form['obj[id]'])
                db_connection.delete_equipment(equipment_id)

                result["result"] = "success"
            except:
                result["result"] = "failture"
            
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )


class RentAccountingsManagement(View, LoginRequiredMixin):
    def get(self, request):

        if request.user.is_anonymous:
            return HttpResponseRedirect("/")
        
        context = base_context(request, title='All rent accountings', header='Записи аренды')
        
        username = request.user.username
        password = request.user.password
        db_connection = DBConnection(username, password)

        context['accountings'] = db_connection.get_all_accountings()
        
        return render(request, "rent_accountings_management.html", context)
    


class SetRentTime(View, LoginRequiredMixin):

    def post(self, request):
        req = request
        form = request.POST

        result = {}
        result["result"] = "failture"

        username = request.user.username
        password = request.user.password
        db_connection = DBConnection(username, password)

        if form["requestType"] == "setStart":
            try:
                time_of_rent = datetime.datetime.now()
                execute = db_connection.set_fact_start_accounting_date(int(form['accounting_id']), time_of_rent)

                result['time_of_start_rent'] = beauty_date(time_of_rent)
                result["result"] = "success"
            except:
                result["result"] = "failture"

        elif form["requestType"] == "setEnd":
            try:
                time_of_rent = datetime.datetime.now()
                execute = db_connection.set_fact_end_accounting_date(int(form['accounting_id']), time_of_rent)

                result['time_of_end_rent'] = beauty_date(time_of_rent)
                result["result"] = "success"
            except:
                result["result"] = "failture"
        
        else:
            result["result"] = "failture"
            
        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )

