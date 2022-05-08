from datetime import datetime
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from django.http import Http404
from .serializer import *
from .models import *



class ProduitCreateApi(generics.CreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitApi(generics.ListAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitDeleteApi(generics.DestroyAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer


class AddProductToCartAPI(generics.CreateAPIView):
    """ endpoint to add a product to an order-cart"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddProductToCartSerilizer


    def post(self, request, *args, **kwargs):
        user = request.user
        item = request.data["item"]
        new_quantity = request.data["quantity"]
        if OrderItem.objects.filter(user=user).filter(item=item).exists():
            OrderItem.objects.filter(user=user).filter(item=item).filter(is_ordered=False).update(
                quantity=new_quantity
            )
        else:
            OrderItem.objects.create(
                user=user,
                item=Produit.objects.filter(id=item).first(),
                quantity=new_quantity
            )

        return Response(
            {'msg': "item added to cart"},
            status=status.HTTP_200_OK)


class RemoveProductToCartAPI(generics.CreateAPIView):
    """ endpoint to remove a product from an order-cart"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RemoveProductToCartSerilizer


    def post(self, request, *args, **kwargs):
        user = request.user
        item = request.data["item"]
        if OrderItem.objects.filter(user=user).filter(item=item).exists():
            OrderItem.objects.filter(user=user).filter(item=item).filter(is_ordered=False).delete()
            return Response(
                {'msg': "item removed from cart"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'msg': "item doesn't exist to any cart"},
                status=status.HTTP_200_OK
            )



class CreateOrderAPI(generics.CreateAPIView):
    """ endpoint to create an order"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateOrderSerilizer

    def post(self, request, *args, **kwargs):
        user = request.user
        order_details = Order.objects.filter(user=user).filter(ordered=False)


    def post(self, request, *args, **kwargs):
        user = request.user

        if Order.objects.filter(user=user).filter(ordered=False).exists():
            return Response(
                {'msg': "Order already exists"},
                status=status.HTTP_200_OK
            )
        else:
            Order.objects.create(
                user=user,
                ref_code=Order.generate_ref_code(self),
                shipping_address=user.address,
                status="Ordered",
                ordered_date=datetime.now()
            )
            Order_item_list = OrderItem.objects.filter(user=user).filter(is_ordered=False)
            order = Order.objects.filter(user=user).filter(ordered=False).first()
            order.shipping_address = user.address

            for order_item in Order_item_list:
                order.items.add(order_item)

            order.save()
            return Response(
                {'msg': "Order created"},
                status=status.HTTP_200_OK)