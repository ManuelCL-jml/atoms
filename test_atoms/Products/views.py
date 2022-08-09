import time

from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from django.db import IntegrityError

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from typing import Dict, Any, ClassVar, List, NoReturn
from Products.error_responses import MyHttpError
from Products.models import Product, Sizes
from Products.serializers import SerializerCreateProduct, SerializerRegisterProductSizes, SerializerRegisterProductTags, \
    SerializerCreateProductImages
from Products.success_response import MyHtppSuccess


# Componente que obtiene los datos ingresados por el usuario
class RequestDataProduct:
    def __init__(self, request_data: Dict[str, Any]):
        self._request_data = request_data

    @property
    def get_name(self) -> str:
        return self._request_data.get('name')

    @property
    def get_sku(self) -> str:
        return self._request_data.get('sku')

    @property
    def get_cost(self) -> str:
        return self._request_data.get('cost')

    @property
    def get_status_id(self) -> str:
        return self._request_data.get('status_id')

    @property
    def get_list_sizes(self) -> List[int]:
        return self._request_data.get('Sizes')

    @property
    def get_list_tags(self) -> List[str]:
        return self._request_data.get('Tags')

    @property
    def get_images_list(self) -> List[Dict[str, Any]]:
        return self._request_data.get('ImagesProduct')


# Componente para crear el producto
class CreateProduct:
    _serializer_class: ClassVar[SerializerCreateProduct] = SerializerCreateProduct
    product_instance: ClassVar[Product]

    def __init__(self, request_data: RequestDataProduct):
        self._request_data = request_data
        self._create()

    @property
    def _data(self) -> Dict[str, Any]:
        return {
            "name": self._request_data.get_name,
            "sku": self._request_data.get_sku,
            "cost": self._request_data.get_cost,
            "status_id": self._request_data.get_status_id
        }

    def _create(self):
        serializer = self._serializer_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        self.product_instance = serializer.create()


# Componente para subir las imagenes en base 64 del producto que se va a registrar
class CreateImageProducts:
    _serializer_class: ClassVar[SerializerCreateProductImages] = SerializerCreateProductImages

    def __init__(self, request_data: RequestDataProduct, producto: CreateProduct):
        self._request_data = request_data
        self._product_id = producto.product_instance.id
        self._create()

    @property
    def _data(self) -> List[Dict[str, Any]]:
        return self._request_data.get_images_list

    @property
    def _context(self) -> Dict[str, Any]:
        return {
            "product_id": self._product_id,
        }

    def _create(self) -> NoReturn:
        for document in self._data:
            serializer = self._serializer_class(data=document, context=self._context)
            serializer.is_valid(raise_exception=True)
            serializer.create()


# Componente para registrar las tallas de los productos
class RegisterProductSizes:
    _serializer_class: ClassVar[SerializerRegisterProductSizes] = SerializerRegisterProductSizes

    def __init__(self, request_data: RequestDataProduct, product: CreateProduct):
        self._request_data = request_data
        self._product = product
        self.create()

    @property
    def _context(self) -> Dict[str, Any]:
        return {
            "product_id": self._product.product_instance.id
        }

    @property
    def _data(self) -> Dict[str, List[int]]:
        return {
            "sizes": self._request_data.get_list_sizes
        }

    def create(self):
        serializer = self._serializer_class(data=self._data, context=self._context)
        serializer.is_valid(raise_exception=True)
        serializer.create()


# Componente para registrar los tags del producto
class RegisterProductTags:
    _serializer_class: ClassVar[SerializerRegisterProductTags] = SerializerRegisterProductTags

    def __init__(self, request_data: RequestDataProduct, product: CreateProduct):
        self._request_data = request_data
        self._product = product
        self.create()

    @property
    def _context(self) -> Dict[str, Any]:
        return {
            "product_id": self._product.product_instance.id
        }

    @property
    def _data(self) -> Dict[str, List[str]]:
        if len(self._request_data.get_list_tags) > 25:
            raise ValueError('Solo se permiten 25 tags')
        return {
            "tags": self._request_data.get_list_tags
        }

    def create(self):
        serializer = self._serializer_class(data=self._data, context=self._context)
        serializer.is_valid(raise_exception=True)
        serializer.create()


# Endpoint para crear un producto
class RegisterProduct(GenericViewSet):
    permission_classes = ()

    def create(self, request):
        try:
            with atomic():
                request_data = RequestDataProduct(request.data)
                product = CreateProduct(request_data)
                CreateImageProducts(request_data, product)
                RegisterProductSizes(request_data, product)
                RegisterProductTags(request_data, product)

        except (ObjectDoesNotExist, IntegrityError, ValueError, TypeError) as e:
            err = MyHttpError(message="Ocurrió un error al momento de registrar el producto", real_error=str(e))
            return Response(err.standard_error_responses(), status=status.HTTP_400_BAD_REQUEST)
        else:
            succ = MyHtppSuccess(message="Su operación se realizo satisfactoriamente", extra_data="")
            return Response(succ.standard_success_responses(), status=status.HTTP_200_OK)


# Endpoint que busca las tallas de los productos con filtro por SKU y por talla
class ListProducts(ListAPIView):
    permission_classes = ()

    @staticmethod
    def render_json(**kwargs) -> Dict[str, Any]:
        return {
            "Talla": int(kwargs.get('size')),
        }

    @staticmethod
    def list_sizes(**kwargs):
        l = Sizes.objects.filter(
            product__sku__icontains=kwargs.get('sku', ''),
            size__icontains=kwargs.get('size', ''),
        ).values('size').order_by('-size')
        return l

    def list(self, request, *args, **kwargs):
        inicio = time.time()
        data = {key: value for key, value in self.request.query_params.items() if value != 'null'}
        externs_clients = self.list_sizes(**data)

        lista = [self.render_json(**i) for i in externs_clients]
        fin = time.time()
        if len(lista) != 0:
            return Response({f"Se encontraron registos": 'success',
                             'Tiempo_transcurrido': fin - inicio,
                             'Tallas': lista,
                             })
        else:
            return Response('No se encontraron registros')





