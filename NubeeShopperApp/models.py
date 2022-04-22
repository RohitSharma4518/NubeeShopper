from distutils.command.upload import upload
from email.policy import default
from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_image = models.ImageField(upload_to = 'NubeeShopperApp/images',default="")
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=500)
    product_price = models.IntegerField(default=0)
    product_category = models.CharField(max_length=50, default="")
    product_subcategory = models.CharField(max_length=50, default="")
    publish_date = models.DateField()

    def __str__(self) -> str:
        return self.product_name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."