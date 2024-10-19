import json
from turtle import title
from django import db
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from common_code.views_functions import *

from decimal import Decimal, ROUND_HALF_UP


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser


from django.views.generic import View
from json import loads

from romantik.settings import BASE_DIR
from .models import *
from datetime import datetime
from .code.db_connect import *


def full_name(user):
    if user.last_name != '' and user.first_name != '':
        return user.first_name+' '+user.last_name
    elif user.first_name != '':
        return user.first_name
    elif user.last_name != '':
        return user.last_name
    else:
        return user.username


def get_all_contacts():
    contacts = []
    for contact in User.objects.all():
        contacts.append((contact.id, contact.username, ""))
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


class KaptyorkaHomePage(View):
    def get(self, request):
        context = base_context(request, title='Kaptyorka', header='Спорядження')
        return render(request, "kaptyorka_homepage.html", context)


class AddEquipment(View, LoginRequiredMixin):
    def get(self, request):

        if request.user.is_anonymous:
            return HttpResponseRedirect("/")

        if request.user.is_superuser:

            context = base_context(request, title='Спорядження', header='Спорядження')
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
                curr_price  = Decimal(form['obj[price]'])
                curr_price = curr_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
                new_equipment = Equipment(
                    name=form['obj[name]'],
                    cathegory=db_connection.get_cathegory_by_path(form['obj[path]']),
                    price=curr_price,
                    img_path="",
                    description=form['obj[desc]'],
                    amount=int(form['obj[amount]'])
                )
                new_equipment.save()
                new_equipment_id = new_equipment.id

                result['new_id'] = new_equipment_id
                result["result"] = "success"
            except:
                result["result"] = "failture"

        elif form["requestType"] == "update":
            try:


                equipment_id = int(form['obj[id]'])
                curr_equipment = Equipment.objects.get(id=equipment_id)
                curr_equipment.name = form['obj[name]']
                curr_equipment.description = form['obj[desc]']
                curr_price  = Decimal(form['obj[price]'])
                curr_equipment.price = curr_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
                curr_equipment.amount = int(form['obj[amount]'])
                curr_equipment.save()

                result["result"] = "success"
            except:
                result["result"] = "failture"

        elif form["requestType"] == "remove":
            try:
                equipment_id = int(form['obj[id]'])
                curr_equipment = Equipment.objects.get(id=equipment_id)
                curr_equipment.delete()

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
