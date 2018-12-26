# encoding: utf-8
from django.db.models import Q

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd, HotSearchWords
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


#商品列表页
class GoodsSerializer(serializers.ModelSerializer):
    #覆盖外键字段
    category = CategorySerializer()
    #images是数据库中设置的related_name="images"，把轮播图嵌套进来
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'



class CategorySerializer3(serializers.ModelSerializer):
    """
    商品三级类别序列化
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    商品二级类别序列化
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    # 首页系列商标一对多
    brands = BrandSerializer(many=True)
    # 首页商品自定义methodfield获取相关类匹配
    goods = serializers.SerializerMethodField()
    # 获取二级类
    sub_cat = CategorySerializer2(many=True)
    # 获取广告商品(一个的)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            # 取到这个商品Queryset[0]
            good_ins = ad_goods[0].goods
            # 在serializer里面调用serializer的话，就要添加一个参数context（上下文request）,嵌套serializer必须加
            # serializer返回的时候一定要加 “.data” ，这样才是json数据
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    # 自定义获取方法
    def get_goods(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"
