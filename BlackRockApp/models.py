from django.db import models
from django.contrib.auth.models import User

TYPE_OF_HIKE = [
	("ПВД", "noncategoried"),
	("Лыжный", "лыжный"),
	("Горный", "горный"),
	("Водный", "водный"),
	("Пеший", "пеший"),
	("Спелео", "спелео"),
	("Вело", "вело"),
]


class Cathegory(models.Model):
    name = models.CharField(max_length=50)
    parent_cathegory = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_cathegory', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cathegory'


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    cathegory = models.ForeignKey(Cathegory, models.DO_NOTHING, db_column='cathegory')
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    img_path = models.CharField(max_length=350)
    description = models.CharField(max_length=2000)
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'equipment'


class OldPriceOfEquipment(models.Model):
    equipment = models.OneToOneField(Equipment, models.DO_NOTHING, db_column='equipment', primary_key=True)
    datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'old_price_of_equipment'
        unique_together = (('equipment', 'datetime'),)


class RentAccounting(models.Model):
    username = models.ForeignKey('Users', models.DO_NOTHING, db_column='username')
    comment = models.CharField(max_length=400)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fact_start_date = models.DateTimeField(blank=True, null=True)
    fact_end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rent_accounting'


class RentedCountableEquipment(models.Model):
    accounting = models.OneToOneField(RentAccounting, models.DO_NOTHING, db_column='accounting', primary_key=True)
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='equipment')
    amount = models.IntegerField()
    returned_amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rented_countable_equipment'
        unique_together = (('accounting', 'equipment'),)


class RentedEquipment(models.Model):
    accounting = models.OneToOneField(RentAccounting, models.DO_NOTHING, db_column='accounting', primary_key=True)
    deterioration = models.IntegerField()
    equipment = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='equipment')

    class Meta:
        managed = False
        db_table = 'rented_equipment'
        unique_together = (('accounting', 'equipment'),)


class UniqueEquipment(models.Model):
    id = models.OneToOneField(Equipment, models.DO_NOTHING, db_column='id', primary_key=True)
    deterioration = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'unique_equipment'


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    confidence_factor = models.IntegerField()
    profile_approved = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users'