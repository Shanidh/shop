from rest_framework import serializers


class ShopUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CustomerListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    username = serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)    


class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()   
    price = serializers.CharField() 


class OrderListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product__name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    quantity = serializers.CharField(read_only=True)  


class ChangeOrderStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)   
    price = serializers.CharField(read_only=True)              