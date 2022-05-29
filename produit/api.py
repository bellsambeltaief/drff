from datetime import datetime
from inspect import stack
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from .serializer import *
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import APIException


class ProduitCreateApi(generics.CreateAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

class ProduitApi(generics.ListAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = (permissions.AllowAny,)
    

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


class GetProductByVendorIdAPI(generics.CreateAPIView):
    """ endpoint to get a product by the vendor id """
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProduitSerializer
    http_method_names = ["get"]  # 'post', 'head', 'put', 'patch'

    def get(self, request, *args, **kwargs):
        user = request.user
        if (
            "vendor_id" not in request.query_params
            or self.request.query_params.get("vendor_id") == ""
        ):
            raise APIHttp400(detail={"errors": {"vendor_id": "Parameter is missing"}})
        else:
            vendor_id = self.request.query_params.get("vendor_id")
            product_list = Produit.objects.filter(vender=vendor_id)
            product_list_serializer =  self.serializer_class(product_list, many=True)
            return Response(
                data=dict(queryset=product_list_serializer.data),
                status=status.HTTP_200_OK
                )



class CreateOrderAPI(generics.CreateAPIView):
    """ endpoint to create an order"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateOrderSerilizer

    def get(self, request, *args, **kwargs):
        user = request.user
        if Order.objects.filter(user=user).filter(ordered=False).exists():
            order_details = Order.objects.filter(user=user).filter(ordered=False).first()                
            return JsonResponse(
                    {
                        "order_ref_code":order_details.ref_code,
                        "order_start_date":order_details.start_date,
                        "order_shipping_address":order_details.shipping_address,
                        "order_status":order_details.status,
                        "order_ref_code":order_details.ref_code,
                        "order_ordered_date":order_details.ordered_date,
                        "order_total_price":str(order_details.get_total()) +" Dinars"
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'msg': "order does not exists"},
                status=status.HTTP_200_OK
                )

    def patch(self, request, *args, **kwargs):
        user = request.user
        if Order.objects.filter(user=user).filter(ordered=False).exists():
            order = Order.objects.filter(user=user).filter(ordered=False).first()
            if order.ordered == False:
                order.ordered = True
                order.status =  "Pending"
                order.save()

                email_message      = 'Bonjour' +' ' +user.email + '\n votre commande est en cours de preparation\n' +"N° commande: " +order.ref_code + '\n\nMerci d utiliser notre site!'
                from_email      = settings.DEFAULT_FROM_EMAIL
                to_email        = [order.user.email]
                email_subject   = 'Confirmation de commande'
                send_mail(
                    email_subject,
                    email_message,           
                    from_email,
                    to_email,
                    fail_silently=False,
                )
                return Response(
                {'msg': "order status updated"},
                status=status.HTTP_200_OK
                )

            else:
                return JsonResponse(
                    {
                        'msg': "Order already confirmed",
                        "order_status":order.status,
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'msg': "order does not exists"},
                status=status.HTTP_200_OK
                )



    def post(self, request, *args, **kwargs):
        user = request.user

        if Order.objects.filter(user=user).filter(ordered=False).exists():
            order = Order.objects.filter(user=user).filter(ordered=False).first()
            return JsonResponse(
                {
                    'msg': "Order already exists",
                    "order_total_price":str(order.get_total()) +" Dinars"
                },
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
            return JsonResponse(
                {
                    'msg': "Order created",
                    "order_total_price":str(order.get_total()) +" Dinars"
                },
                status=status.HTTP_200_OK)



class AddProductToWishlistAPI(generics.CreateAPIView):
    """ endpoint to add a product to wishlist"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddProductToWishlistSerilizer


    def post(self, request, *args, **kwargs):
        user = request.user
        item = request.data["item"]
        new_quantity = request.data["quantity"]
        if WishlistItem.objects.filter(user=user).filter(item=item).exists():
            WishlistItem.objects.filter(user=user).filter(item=item).filter(is_confirmed=False).update(
                quantity=new_quantity
            )
            updated_item = WishlistItem.objects.filter(user=user).filter(item=item).filter(is_confirmed=False).first()
        else:
            updated_item = WishlistItem.objects.create(
                user=user,
                item=Produit.objects.filter(id=item).first(),
                quantity=new_quantity
            )
        if Wishlist.objects.filter(user=user).filter(is_confirmed=False).exists():
            wishlist = Wishlist.objects.filter(user=user).filter(is_confirmed=False).first()
            wishlist.items.add(updated_item)
        return Response(
            {'msg': "item added to wishlist"},
            status=status.HTTP_200_OK)

    
    def delete(self, request, *args, **kwargs):
        user = request.user
        if (
            "item" not in request.data
        ):
            return Response(
                {'msg': "Item details are missing"},
                status=status.HTTP_404_NOT_FOUND)
        else:
            item = request.data["item"]

            if WishlistItem.objects.filter(user=user).filter(item=item).filter(is_confirmed=False).exists():
                wishlist = WishlistItem.objects.filter(user=user).filter(item=item).filter(is_confirmed=False).first()
                wishlist.delete()
                return Response(
                    {
                        'msg': "item removed from wishlist"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                {'msg': "item does not exist to the wishlist"},
                status=status.HTTP_404_NOT_FOUND)


class CreateWishlistAPI(generics.CreateAPIView):
    """ endpoint to create an order"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateWishlistSerilizer

    def get(self, request, *args, **kwargs):
        user = request.user
        if Wishlist.objects.filter(user=user).filter(is_confirmed=False).exists():
            reponse_data = []
            wishlist_details = Wishlist.objects.filter(user=user).filter(is_confirmed=False).first()     
            for item in wishlist_details.items.all():
                item_detail = {
                    "prod_name":item.item.prod_name,
                    "price":str(item.item.price) +" Dinars",
                    "category":item.item.category,
                    "category":item.item.category,
                    "image" :"http://localhost:8000"+ str(item.item.image.url) if item.item.image else "None",
                }
                reponse_data.append(item_detail)

            return JsonResponse(
                    {
                        "wishlist_total_price":str(wishlist_details.get_total()) +" Dinars",
                        "wishlist":reponse_data,
                    },
                    status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'msg': "wishlist does not exists"},
                status=status.HTTP_200_OK
                )


    def post(self, request, *args, **kwargs):
        user = request.user

        if Wishlist.objects.filter(user=user).filter(is_confirmed=False).exists():
            wishlist = Wishlist.objects.filter(user=user).filter(is_confirmed=False).first()
            return JsonResponse(
                {
                    'msg': "Wishlist already exists",
                },
                status=status.HTTP_200_OK
            )
        else:
            Wishlist.objects.create(
                user=user,
            )
            wishlist_item_list = WishlistItem.objects.filter(user=user).filter(is_confirmed=False)
            wishlist = Wishlist.objects.filter(user=user).filter(is_confirmed=False).first()

            for order_item in wishlist_item_list:
                wishlist.items.add(order_item)

            wishlist.save()
            return JsonResponse(
                {
                    'msg': "Order created",
                    "wishlist_total_price":str(wishlist.get_total()) +" Dinars"
                },
                status=status.HTTP_200_OK)




class APIHttp400(APIException):
    """API Http 400 Error"""

    status_code = 400