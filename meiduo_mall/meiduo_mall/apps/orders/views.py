from decimal import Decimal
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from orders.serializers import OrderSettlementSerializer, SaveOrderSerializer


class OrderSettlementView(APIView):
    '''订单结算'''
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # 获取用户对象  user
        user = request.user

        # 从redis中查询购物车  sku_id  count  selected
        redis_conn = get_redis_connection('cart')

        # hash  商品数量 sku_id  count
        redis_cart_dict = redis_conn.hgetall('cart_%s' % user.id)

        # set 勾选商品
        redis_cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)

        cart = {}
        # cart = {
        #   勾选商品信息
        #   sku_id: count
        # }
        for sku_id in redis_cart_selected:
            cart[int(sku_id)] = int(redis_cart_dict[sku_id])

        sku_id_list = cart.keys()
        sku_object_list = SKU.objects.filter(id__in=sku_id_list)

        for sku in sku_object_list:
            sku.count = cart[sku.id]

        freight = Decimal('10.00')

        serializer = OrderSettlementSerializer({'freight':freight,'skus':sku_object_list})
        return Response(serializer.data)

class SaveOrderView(CreateAPIView):
    '''保存订单'''
    serializer_class = SaveOrderSerializer
    permission_classes = [IsAuthenticated]

