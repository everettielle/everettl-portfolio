from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
import os


# Create your models here.
class Condition(models.Model):
    condition = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.condition


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    pictures = models.JSONField()
    price = models.IntegerField()
    shipping_fee = models.IntegerField()
    returnable = models.BooleanField()
    sold = models.BooleanField(default=False)
    is_auction = models.BooleanField()
    condition = models.ForeignKey(Condition, null=True, on_delete=models.SET_NULL)  # CASCADE -> SET_NULL
    published_date = models.DateTimeField(default=timezone.now)
    published_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewer = models.IntegerField(default=0)
    like = models.IntegerField(default=0)

    def __str__(self):
        return "{} ({}): {}".format(self.id, self.published_user.username, self.title)


# 제품 이미지 다중 업로드를 위한 모델
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_image", on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=f'auction/{timezone.now().strftime("%Y/%m/%f")}/')

    def __str__(self):
        return "{}: {}".format(self.id, self.product.id)


# 제품 이미지 삭제 시 서버에서 일괄 삭제
def delete_image(sender, instance, **kwargs):
    if instance.image:
        path = instance.image.path
        try:
            os.remove(path)
        except:
            pass


models.signals.post_delete.connect(delete_image, sender=ProductImage)


class Auction(models.Model):
    product = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()
    current_price = models.IntegerField()
    bids = models.JSONField()

    def __str__(self):
        return str(self.product.id) + ": " + self.product.title


class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    published_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()

    def __str__(self):
        return "{}: {} -> {}, {}₩".format(self.id, self.published_user.username, self.product, self.price)