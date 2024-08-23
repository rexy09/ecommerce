from common.exception_response import exception_handler
from common.pagination import CustomPagination
from .filters import ProductFilter
from .serializers import CategorySerializer, OrderListSerializer, OrderPaySerializer, OrderSerializer, ProductListSerializer, ProductSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

# Create your views here.


@api_view(['GET', 'POST', 'PUT'])
def category(request):
    if request.method == "POST":
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                response = CategorySerializer(instance).data
                return Response(response)

            except Exception as e:
                return exception_handler(e)
        else:
            response = {
                "message": serializer.errors, "status": 'error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        data = request.data
        category_instance = Category.objects.filter(id=data["id"]).first()
        serializer = CategorySerializer(category_instance, data=data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                response = CategorySerializer(instance).data
                return Response(response)

            except Exception as e:
                return exception_handler(e)
        else:
            response = {
                "message": serializer.errors, "status": 'error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        try:
            queryset = Category.objects.all().order_by('name')
            data = CategorySerializer(
                queryset, many=True).data

            return Response(data)
        except Exception as e:
            response = {
                "message": 'Error something went wrong', "status": 'error'}
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'PUT'])
def product(request):
    if request.method == "POST":
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                response = ProductSerializer(instance).data
                return Response(response)

            except Exception as e:
                return exception_handler(e)
        else:
            response = {
                "message": serializer.errors, "status": 'error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        data = request.data
        product_instance = Product.objects.filter(id=data["id"]).first()
        serializer = ProductSerializer(product_instance, data=data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                response = ProductSerializer(instance).data
                return Response(response)

            except Exception as e:
                return exception_handler(e)
        else:
            response = {
                "message": serializer.errors, "status": 'error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        try:

            paginator = CustomPagination()
            paginator.page_size = 2
            queryset = Product.objects.filter(
            ).select_related('category').all()
            filter = ProductFilter(request.GET, queryset)
            result_page = paginator.paginate_queryset(filter.qs, request)
            response = ProductListSerializer(
                result_page, many=True).data
            return paginator.get_paginated_response(response)

        except Exception as e:
            response = {
                "message": 'Error something went wrong', "status": 'error'}
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST',])
def order(request):
    if request.method == "POST":
        data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            try:
                customer, _ = Customer.objects.get_or_create(
                    full_name=data['full_name'])

                instance = serializer.save(customer=customer)
                amount = instance.product.price * instance.quantity
                instance.total_amount = amount
                instance.save()
                response = OrderListSerializer(instance).data
                return Response(response)

            except Exception as e:
                return exception_handler(e)
        else:
            response = {
                "message": serializer.errors, "status": 'error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        try:

            paginator = CustomPagination()
            paginator.page_size = 10
            queryset = Order.objects.filter(
            ).select_related('customer', 'product').all()
            result_page = paginator.paginate_queryset(queryset, request)
            response = OrderListSerializer(
                result_page, many=True).data
            return paginator.get_paginated_response(response)

        except Exception as e:
            response = {
                "message": 'Error something went wrong', "status": 'error'}
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST',])
def pay_order(request):
    if request.method == "POST":
        data = request.data
        serializer = OrderPaySerializer(data=data)
        if serializer.is_valid():
            try:
                order_instance = Order.objects.filter(
                    id=data["id"]).first()

                order_instance.payment_type = serializer.validated_data.get("payment_type")
                order_instance.paid = True
                order_instance.status = "paid"
                order_instance.save()
                order_data = OrderListSerializer(order_instance).data
                response = {
                    "message": 'Order paid successful', "status": 'success', 'data': order_data}
                return Response(response)

            except Exception as e:
                return exception_handler(e)
        else:
            response = {
                "message": serializer.errors, "status": 'error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


