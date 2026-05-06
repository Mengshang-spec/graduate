from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from userapp.models import UserInfo,Area,Address
from django.http import JsonResponse
from django.core.serializers import serialize
from cartsapp.cartmanager import getCartManger
from cartsapp.models import *
import jsonpickle


def order_View(request):
    cartitems  = request.GET.get('cartitems','')
    user  = request.session.get('user','')
    if not user:
        return HttpResponseRedirect('/user/login/?redirct=order&cartitems'+cartitems)
    return HttpResponseRedirect('/order/toOrder/?cartitems='+cartitems)
# Create your views here.
def toOrder(request):
    cartitems = request.GET.get('cartitems','')
    cartitemsList =  jsonpickle.loads(cartitems)
    cartitemsObjList = [ getCartManger(request).get_cartitems(**ci) for ci in cartitemsList if ci]
    user = jsonpickle.loads(request.session.get('user'))
    addr = user.address_set.get(isdefault=True)
    totalPrice = 0
    for cio in cartitemsObjList:
        totalPrice += cio.getTotalPrice()
    return render(request,'order.html',{'cartitemsList':cartitemsObjList,'addr':addr,'totalPrice':totalPrice})

