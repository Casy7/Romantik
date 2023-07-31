from django.contrib import admin

from .models import *

# Для регистрации модели добавить её в models
models = [Equipment, Cathegory, OldPriceOfEquipment, RentAccounting, RentedCountableEquipment, RentedEquipment, UniqueEquipment, Users, 
]

for model in models:
    admin.site.register(model)