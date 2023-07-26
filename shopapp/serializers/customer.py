from rest_framework import serializers


class CustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateCustomerSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()    


class CustomerProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)   
    price = serializers.CharField(read_only=True)    


class CustomerCartSerializer(serializers.Serializer):
    products = serializers.CharField(read_only=True) 


class CustomerOrderProductSerializer(serializers.Serializer):
    product_id = serializers.CharField() 
    quantity = serializers.CharField()    


class CustomerOrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product__name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    quantity = serializers.CharField(read_only=True)          