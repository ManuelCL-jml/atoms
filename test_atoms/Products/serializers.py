from rest_framework.serializers import *

from drf_extra_fields.fields import Base64ImageField
from Products.models import Product, Images, Tags, Status, Sizes
from typing import Dict, Any, ClassVar, List


# Serializador para registrar un producto
class SerializerCreateProduct(Serializer):
    name = CharField()
    sku = CharField()
    cost = FloatField()
    status_id = IntegerField()

    def validate(self, attrs):
        if attrs['status_id'] > 3:
            raise ValidationError('El estado que ingreso no es valido')
        return attrs

    def create(self, **kwargs) -> Product:
        return Product.objects.create_product(**self.validated_data)


# Serializador para guardar las imagenes del producto
class SerializerCreateProductImages(Serializer):
    documento = Base64ImageField(allow_null=False, required=True)
    product_id = IntegerField(read_only=True)

    def validate(self, attrs):
        attrs['product_id'] = self.context.get('product_id')
        return attrs

    def create(self, **kwargs) -> Images:
        return Images.objects.create(**self.validated_data)


# Serializador para registrar las tallas de los productos
class SerializerRegisterProductSizes(Serializer):
    sizes = ListField()

    def validate_sizes_list(self, value: List[int]):
        return value

    def validate(self, attrs):
        return attrs

    def create(self, **kwargs):
        objs = [
            Sizes.objects.register_sizes(size=i, **self.context)
            for i in self.validated_data.get('sizes')
        ]
        Sizes.objects.bulk_create(objs)


# Serializador para guardar los tags de los productos
class SerializerRegisterProductTags(Serializer):
    tags = ListField()

    def validate_sizes_list(self, value: List[int]):
        return value

    def validate(self, attrs):
        tags_register = Tags.objects.filter(product_id=self.context['product_id']).count()
        if tags_register > 25:
            raise ValidationError('Solo se permiten 25 tags por producto')
        return attrs

    def create(self, **kwargs):
        objs = [
            Tags.objects.register_tags(tag=i, **self.context)
            for i in self.validated_data.get('tags')
        ]
        Tags.objects.bulk_create(objs)

