from django.contrib.auth.models import User
from rest_framework import serializers
from rest_srv.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('url', 'restaurant_name')


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('url', 'id', 'city', 'street', 'address_num', 'door_num')


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(many=False, read_only=False)

    class Meta:
        model = Client
        fields = ('url', 'id', 'first_name', 'last_name', 'phone_number', 'address')

    def create(self, validated_data):
        address_data = validated_data.pop('address')

        address = None
        if Address.objects.filter(**address_data).exists():
            address = Address.objects.get(**address_data)
        else:
            address = Address.objects.create(**address_data)
            address.save()
        client = Client.objects.create(address=address, **validated_data)
        return client


class DishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dish
        fields = ('url', 'name', 'quantity')


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(many=False, read_only=False)

    class Meta:
        model = Restaurant
        fields = ('url', 'address', 'name')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address, acreated = Address.objects.get_or_create(**address_data)

        if acreated:
            address.save()

        restaurant = Restaurant.objects.create(address=address, **validated_data)
        return restaurant


class OrderSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)
    client = ClientSerializer(many=False, read_only=False)
    restaurant = RestaurantSerializer(many=False, read_only=False)

    class Meta:
        model = Order
        fields = ('url', 'dishes', 'client', 'restaurant')

    def create(self, validated_data):
        dishes = []
        restaurant_data = {}
        restaurant_addr_data = {}
        client_data = {}
        client_addr_data = {}

        if 'dishes' in validated_data:
            dishes = validated_data.pop('dishes')
        if 'restaurant' in validated_data:
            restaurant_data = validated_data.pop('restaurant')
        if 'address' in restaurant_data:
            restaurant_addr_data = restaurant_data.pop('address')
        if 'client' in validated_data:
            client_data = validated_data.pop('client')
        if 'address' in client_data:
            client_addr_data = client_data.pop('address')

        restaurant_addr = Address.objects.create(**restaurant_addr_data)
        restaurant_addr.save()
        restaurant = Restaurant.objects.create(**restaurant_data, address=restaurant_addr)
        restaurant.save()

        client_addr = Address.objects.create(**client_addr_data)
        client_addr.save()
        client = Client.objects.create(**client_data, address=client_addr)
        client.save()

        order = Order.objects.create(**validated_data, client=client, restaurant=restaurant)
        order.save()

        # restaurant = Restaurant.objects.create(**)

        # client = Client()

        for dish in dishes:
            d, created = Dish.objects.get_or_create(order=order, **dish)
            if created is True:
                d.save()

        return order



# Tworzenie restauracji -> przykład
# metodą POST wysyłamy na address 127.0.0.1:8000/restaurants/ to coś: {"menu": {"dishes": [{"name": "burak"}]}, "address": {"city": "warsaw"}}
# w bazie utworzy się restauracja z menu które będzie posiadało lisę dań oraz obiekt adresu,
# innymi słowy w bazie utworzą się rekordy w 4 tabelach: restaurant, dishes, menu, address