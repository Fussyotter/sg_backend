from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    productName = models.CharField(max_length=100)
    productCode = models.CharField(max_length=150)
    total = models.IntegerField(
        default=0, null=True, blank=True, verbose_name='Total Count')
    user = models.ManyToManyField(User)
    completed = models.BooleanField()
    def __str__(self): return self.productName


class Supply(models.Model):
    productName = models.CharField(max_length=100)
    productCode = models.CharField(max_length=150)
    stock = models.IntegerField()
    location = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Supplies"

    def __str__(self): return self.productName
