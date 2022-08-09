from django.db import models

# Create your models here.
from Products.managerProduct import ProductManager, SizeManager, TagsManager


class Status(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=30)


class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    sku = models.CharField(max_length=50, null=False, blank=False, unique=True)
    cost = models.FloatField(null=False, blank=False)
    creation_date = models.DateTimeField(auto_now=True)
    date_modify = models.DateTimeField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING,blank=False, null=False, default=1)

    objects = ProductManager()


class Sizes(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    size = models.CharField(max_length=50, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False, null=False)
    objects = SizeManager()


class Tags(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    tag = models.CharField(max_length=50, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False, null=False)
    objects = TagsManager()


class Images(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="user_doctos")
    load = models.DateTimeField(auto_now=True)
    documento = models.FileField(upload_to='documento', default="No se cargo el documento")



