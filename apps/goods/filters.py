from django.db.models import Q

from rest_framework import generics
from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
    '''
    商品过滤的类
    '''
    # 两个参数，name是要过滤的字段，lookup是执行的行为，‘小与等于本店价格’
    price_min = filters.NumberFilter(name="shop_price", lookup_expr='gte', help_text=('大于等于本店价格'))
    price_max = filters.NumberFilter(name="shop_price", lookup_expr='lte', help_text=('小于等于本店价格'))
    top_category = filters.NumberFilter(name="category", method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 不管当前点击的是一级分类二级分类还是三级分类，都能找到。
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot', 'is_new']
