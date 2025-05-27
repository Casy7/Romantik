"""BlackRockProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path
from django.urls import path

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from romantik import settings

from .views import *

urlpatterns = [
    path("", KaptyorkaHomePage.as_view(), name="kaptyorka_home"),
    path("add_equipment", AddEquipment.as_view(), name="add_equipment"),
    path("new_rent_accounting", CreateNewRentAccounting.as_view(), name="new_rent_accounting"),
    path("my_rent_accountings", MyRentAccountings.as_view(), name="my_rent_accountings"),
    path("rent_accountings_management", RentAccountingsManagement.as_view(), name="rent_accountings_management"),


	path('add_accounting/', AjaxAddNewAccounting.as_view(), name='add_accounting'),
	re_path('add_equipment/', AddNewEquipment.as_view(), name='add_equipment'),
    re_path('set_rent_time/', SetRentTime.as_view(), name='set_rent_time'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
