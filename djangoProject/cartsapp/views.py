from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from cartsapp.cartmanager import *
from django.http import HttpResponse,HttpResponseRedirect
class CartView(View):
    def get(self, request):
        red = request.GET.get('redirct','')
        return render(request,'login.html',{'red':red})
    def post(self, request):

        request.session.modified = True
        flag = request.POST.get('flag')
        if flag == 'add':
            cartManger=getCartManger(request)
            cartManger.add(**request.POST.dict())
        elif flag == 'plus':
            cartManger=getCartManger(request)
            cartManger.update(step = 1,**request.POST.dict())
        elif flag == 'minus':
            cartManger = getCartManger(request)
            cartManger.update(step = -1, **request.POST.dict())
        elif flag == 'delete':
            cartManger = getCartManger(request)
            cartManger.delete( **request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')
def queryAll(request):
    cartManger = getCartManger(request)
    cartItemList =  cartManger.queryAll()
    return render(request,'cart.html',{'cartItemList':cartItemList})
