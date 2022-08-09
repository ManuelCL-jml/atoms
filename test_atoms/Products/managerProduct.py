from django.db.models import Manager
import datetime


# Manager para registrar productos
class ProductManager(Manager):
    def create_product(self, **kwargs):
        product = self.model(
            name=kwargs.get('name'),
            sku=kwargs.get('sku'),
            cost=kwargs.get('cost'),
            status_id=kwargs.get('status_id'),
            creation_date=datetime.datetime.now(),
            date_modify=datetime.datetime.now(),
        )

        product.save(using=self._db)
        return product


# Manager para registrar tallas
class SizeManager(Manager):
    def register_sizes(self, **kwargs):
        return self.model(
            size=kwargs.get('size'),
            product_id=kwargs.get('product_id'),
        )


# Manager para registrar tags
class TagsManager(Manager):
    def register_tags(self, **kwargs):
        return self.model(
            tag=kwargs.get('tag'),
            product_id=kwargs.get('product_id'),
        )

