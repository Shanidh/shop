import sys
import requests
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from shopapp.models import CustomUser, UserType
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated

from ..models import Product, Order, OrderStatus

from ..serializers import (
    ShopUserSerializer,
    CustomerListSerializer,
    CreateProductSerializer,
    OrderListSerializer,
    ChangeOrderStatusSerializer,
    ProductListSerializer,
)

from ..services import (
    create_product,
    change_order_status,
)


class LoginAPI(APIView):
    """API for Admin Login."""

    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = ShopUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == UserType.SHOP:
                # Login successful, return user data
                login(request, user)
                data = {
                   "Success": True,
                   "msg": "Login Success",
                }
                return Response(status=status.HTTP_201_CREATED, data=data)
                # return redirect("shopapp:customer_list") 
            else:
            # Login failed
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        

class LogOutAPI(APIView):
    """API for Logout."""
    def get(self, request):
        logout(request)
        return redirect("shopapp:login") 


class CustomerListAPI(APIView):
    """API for getting Post list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = CustomUser.objects.filter(user_type=UserType.CUSTOMER).values("id", "username", "created_date").order_by("-created_date")
            serializer = CustomerListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)    


class CreateProductAPI(APIView):
    """API for creating product for Shop"""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = CreateProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                create_product(user=user, **serializer.validated_data)
                data = {
                    "Success": True,
                    "msg": "New product created.",
                }
            return Response(status=status.HTTP_200_OK, data=data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "Creating product failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)      


class DeleteProductAPI(APIView):
    def post(self, request, id):
        product=Product.objects.get(id=id).delete()
        return product  


class UpdateProductAPI(APIView):
    def post(self, request, id):
        product = Product.objects.get(id=id)
        name = request.query_params.get(name)
        description = request.query_params.get(description)
        price = request.query_params.get(price)
        if name not in ["", None]:
            product.name = name
        if description not in ["", None]:
            product.description = description
        if price not in ["", None]:
            product.price = price  
        product.save()                      


class OrderListAPI(APIView):
    """API for getting order list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = Order.objects.all().values("id", "product__name", "status", "quantity").order_by("-created_date")
            serializer = OrderListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)        


class ChangeOrderStatusAPI(APIView):
    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        try:
            serializer = ChangeOrderStatusSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                result = change_order_status(user=user, **serializer.validated_data)
            return Response(
                status=status.HTTP_201_CREATED,
                data=result,
            )
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "Change status getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)    


class ProductListAPI(APIView):
    """API for getting Product list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = Product.objects.all().values("id", "name", "description", "price").order_by("-created_date")
            serializer = ProductListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)              