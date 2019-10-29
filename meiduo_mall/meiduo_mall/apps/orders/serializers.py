import logging
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import SKU
from .models import OrderInfo, OrderGoods

logger = logging.getLogger('django')

class CarSKUSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(label='数量')
    class Meta:
        model = SKU
        fields = ('id','name','default_image_url','price','count')

class OrderSettlementSerializer(serializers.Serializer):
    '''订单结算数据序列化器'''
    freight = serializers.DecimalField(label='运费',max_digits=10,decimal_places=2)
    skus = CarSKUSerializer(many=True)

class SaveOrderSerializer(serializers.ModelSerializer):
    '''保存订单序列化器'''
    class Meta:
        model = OrderInfo
        fields = ('address','pay_method','order_id')
        read_only_fields = ('order_id',)
        extra_kwargs = {
           'address':{
               'write_only':True
           },
            'pay_method':{
                'required': True
            },

        }

    def create(self, validated_data):
        """
        保存订单
        :param validated_data:
        :return:
        """
        # 保存订单
        address = validated_data['address']
        pay_method = validated_data['pay_method']
        # 获取用户对象
        user = self.context['request'].user
        # 查询购物车redis,链接redis
        redis_conn = get_redis_connection('cart')
        # 商品数量,用hgetall
        redis_cart_dict = redis_conn.hgetall('cart_%s' % user.id)
        # 勾选商品
        redis_cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
        # 勾选商品信息
        cart = {}
        for sku_id  in redis_cart_selected:
            cart[int(sku_id)] = int(redis_cart_dict[sku_id])

        if not cart:
            raise serializers.ValidationError('没有结算商品哈')

        # 创建事务
        with transaction.atomic():
            try:
                # 创建保存点
                save_id = transaction.savepoint()
                # 创建订单编号
                order_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
                order = OrderInfo.objects.create(
                    order_id = order_id,
                    user = user,
                    address = address,
                    total_count = 0,
                    total_amount = Decimal('0'),
                    freight = Decimal('10.00'),
                    pay_method = pay_method,
                    status =OrderInfo.ORDER_STATUS_ENUM['UNSEND'] if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH'] else OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                )
                # 查询数据库，获取商品数据
                sku_id_list = cart.keys()
                # sku_object_list = SKU.objects.filter(id__in=sku_id_list)
                #遍历需要结算的上商品数据
                for sku_id in sku_id_list:
                    while True:
                        sku = SKU.objects.get(id=sku_id)
                        sku_count = cart[sku.id]
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        if origin_stock < sku_count:
                            transaction.savepoint_rollback(save_id)
                            raise serializers.ValidationError('%s库存不足' % sku_id)
                        # import time
                        # time.sleep(5)
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count
                        # 返回受影响的行数
                        result = SKU.objects.filter(id=sku.id,stock=origin_stock).update(stock=new_stock,sales=new_sales)
                        if result == 0:
                            continue
                        order.total_count += sku_count
                        order.total_amount += (sku.price * sku_count)

                        OrderGoods.objects.create(
                            order=order,
                            sku = sku,
                            count = sku_count,
                            price = sku.price
                        )
                        break
                order.save()
            except serializers.ValidationError:
                raise
            except Exception as ret:
                logger.error(ret)
                transaction.savepoint_rollback(save_id)
                raise
            else:
                transaction.savepoint_commit(save_id)
        # 删除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('cart_%s' % user.id,*redis_cart_selected)
        pl.srem('cart_selected_%s' % user.id,*redis_cart_selected)
        pl.execute()

        return order




                # 保存订单

