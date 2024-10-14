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
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    img_path = models.CharField(max_length=350)
    description = models.CharField(max_length=2000)
    amount = models.IntegerField()



class OldPriceOfEquipment(models.Model):
    equipment = models.OneToOneField(Equipment, models.DO_NOTHING, primary_key=True)
    datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        unique_together = (('equipment', 'datetime'),)


class RentAccounting(models.Model):
    username = models.ForeignKey(User, models.DO_NOTHING)
    comment = models.CharField(max_length=400)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fact_start_date = models.DateTimeField(blank=True, null=True)
    fact_end_date = models.DateTimeField(blank=True, null=True)



class RentedCountableEquipment(models.Model):
    accounting = models.OneToOneField(RentAccounting, models.DO_NOTHING, primary_key=True)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)
    amount = models.IntegerField()
    returned_amount = models.IntegerField()

    class Meta:
        unique_together = (('accounting', 'equipment'),)


class RentedEquipment(models.Model):
    accounting = models.OneToOneField(RentAccounting, models.DO_NOTHING, primary_key=True)
    deterioration = models.IntegerField()
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING)

    class Meta:
        unique_together = (('accounting', 'equipment'),)


class UniqueEquipment(models.Model):
    id = models.OneToOneField(Equipment, models.DO_NOTHING, primary_key=True)
    deterioration = models.IntegerField()


