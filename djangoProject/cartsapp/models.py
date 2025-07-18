from django.db import models
from userapp.models import UserInfo
from goodsapp.models import Color, Goods, Size
import math


# Create your models here.c
class CartItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count= models.PositiveIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    def getColor(self):
        return Color.objects.get(id=self.colorid)
    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)
    def getSize(self):
        return Size.objects.get(id=self.sizeid)
    def getTotalPrice(self):
        return math.ceil(int(self.count) * self.getGoods().price)



