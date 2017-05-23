from django.db import models
from django.utils.timezone import now


class Address(models.Model):
    city = models.CharField(max_length=30, default='')
    street = models.CharField(max_length=30, default='')
    address_num = models.CharField(max_length=30, default='')
    door_num = models.CharField(max_length=30, default='')


class Client(models.Model):
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=30, default='')
    phone_number = models.CharField(max_length=15, default='')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Dish(models.Model):
    name = models.CharField(max_length=20, default='')
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='dishes', on_delete=models.CASCADE)


#{"client": {"address": {}}, "dishes": [{"name": "z", "quantity": 122}, {"name": "kabanos", "quantity": 666}], "restaurant": {"name": "Nie jedz tu", "address":{"city": "xxx"}}}