
import xadmin
from xadmin import views

from . import models


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)
class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "美多商城运营管理系统"  # 设置站点标题
    site_footer = "美多商城集团有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)


class SKUAdmin(object):
    list_display = ['id', 'name', 'price', 'stock', 'sales', 'comments']
    list_editable = ['price', 'stock']
    model_icon = 'fa fa-gift'



class SKUSpecificationAdmin(object):
    def save_models(self):
        # 保存数据对象
        obj = self.new_obj
        obj.save()

        # 补充自定义行为
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self):
        # 删除数据对象
        obj = self.obj
        sku_id = obj.sku.id
        obj.delete()

        # 补充自定义行为
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(sku_id)

xadmin.site.register(models.GoodsCategory)
xadmin.site.register(models.GoodsChannel)
xadmin.site.register(models.Goods)
xadmin.site.register(models.Brand)
xadmin.site.register(models.GoodsSpecification)
xadmin.site.register(models.SpecificationOption, SKUSpecificationAdmin)
xadmin.site.register(models.SKU, SKUAdmin)
xadmin.site.register(models.SKUSpecification)
xadmin.site.register(models.SKUImage)


# class SKUAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(obj.id)
#
#
# class SKUSpecificationAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         obj.save()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(obj.sku.id)
#
#     def delete_model(self, request, obj):
#         sku_id = obj.sku.id
#         obj.delete()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(sku_id)
#
#
# class SKUImageAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         # obj -> SKUImage 对象  obj.sku
#
#         obj.save()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(obj.sku.id)
#
#         # 设置SKU默认图片
#         sku = obj.sku
#         if not sku.default_image_url:
#
#             # http://image.meiduo.site:8888/groupxxxxxx
#             sku.default_image_url = obj.image.url
#             sku.save()
#
#     def delete_model(self, request, obj):
#         sku_id = obj.sku.id
#         obj.delete()
#         from celery_tasks.html.tasks import generate_static_sku_detail_html
#         generate_static_sku_detail_html.delay(sku_id)


# xadmin.site.register(models.GoodsCategory)
# xadmin.site.register(models.GoodsChannel)
# xadmin.site.register(models.Goods)
# xadmin.site.register(models.Brand)
# xadmin.site.register(models.GoodsSpecification)
# xadmin.site.register(models.SpecificationOption)
# xadmin.site.register(models.SKU)
# xadmin.site.register(models.SKUSpecification)
# xadmin.site.register(models.SKUImage)