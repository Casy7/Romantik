from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

TYPE_OF_HIKE = [
	("ПВД", "uncategorized"),
	("Лижний", "лижний"),
	("Гірський", "гірський"),
	("Водний", "водний"),
	("Піший", "піший"),
	("Спелео", "спелео"),
	("Вело", "вело"),
]


class Cathegory(models.Model):
    name = models.CharField(max_length=50)
    parent_cathegory = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)



class Equipment(models.Model):
    name = models.CharField(max_length=50)
    cathegory = models.ForeignKey(Cathegory, models.DO_NOTHING)
    price = models.DecimalField(max_digits=63, decimal_places=2)
    img_path = models.CharField(max_length=350)
    description = models.CharField(max_length=2000)
    amount = models.IntegerField()



class OldPriceOfEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, models.CASCADE)
    datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=63, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = (('equipment', 'datetime'),)


class Client(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25)
    telegram = models.CharField(max_length=35)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)


class RentAccounting(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete = models.DO_NOTHING)
    comment = models.CharField(max_length=400)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fact_start_date = models.DateTimeField(blank=True, null=True)
    fact_end_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    is_free = models.BooleanField(default=False)



class RentedCountableEquipment(models.Model):
    accounting = models.ForeignKey(RentAccounting, models.CASCADE)
    equipment = models.ForeignKey(Equipment, blank=True, null=True, on_delete = models.DO_NOTHING)
    amount = models.IntegerField()
    returned_amount = models.IntegerField(default=0)

    class Meta:
        unique_together = (('accounting', 'equipment'),)


class RentedEquipment(models.Model):
    accounting = models.ForeignKey(RentAccounting, models.DO_NOTHING, primary_key=True)
    deterioration = models.IntegerField()
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)

    class Meta:
        unique_together = (('accounting', 'equipment'),)


class UniqueEquipment(models.Model):
    id = models.ForeignKey(Equipment, models.DO_NOTHING, primary_key=True)
    deterioration = models.IntegerField()


