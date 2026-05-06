from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from userapp.models import UserInfo,Area,Address
from django.http import JsonResponse
from django.core.serializers import serialize
from cartsapp.cartmanager import SessionCartManager
import jsonpickle
from jsonpickle import loads as jsonpickle_loads
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        account = request.POST.get('account')
        pwd = request.POST.get('password')

        user = UserInfo.objects.create(uname=account, pwd=pwd)
        if user:
            request.session['user'] = jsonpickle.dumps(user)
            return HttpResponseRedirect('/user/center')
        return HttpResponseRedirect('/user/register')
class CenterView(View):
    def get(self, request):
        return render(request,'center.html')
class LoginView(View):
    def get(self, request):
        red = request.GET.get('redirct','')
        return render(request,'login.html',{'red':red,'cartitems':request.GET.get('cartitems','')})
    def post(self, request):
        uname = request.POST.get('account','')
        pwd = request.POST.get('password','')
        redi = request.POST.get('redirect','')
        userList = UserInfo.objects.filter(uname = uname, pwd = pwd)
        #判断是否登录
        if userList:
            request.session['user'] =jsonpickle.dumps( userList[0])
            SessionCartManager(request.session).migrateSession2DB()
            if redi == 'cart':

                return HttpResponseRedirect('/cart/queryAll/')
            elif redi == 'order':
                return HttpResponseRedirect('/order/toOrder/?cartitems='+request.POST.get('cartitems',''))
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')
from utils.code import *

class LoadCodeView(View):
    def get(self, request):
        img,txt = gene_code()
        # txt保存在session
        request.session['sessionCode']= txt
        return HttpResponse(img,content_type='image/png')
class CheckCodeView(View):
    def get(self, request):
        code = request.GET.get('code','')
        sessioncode = request.session.get('sessionCode')
        flag = code == sessioncode

        return JsonResponse({'flag':flag})
class Logout(View):
    def get(self, request):
        request.session.clear()
        return JsonResponse({'flag':True})


class AddressView(View):
    def get(self, request):
        user = jsonpickle.loads(request.session.get('user'))
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList': addrList})

    def post(self, request):
        params = request.POST.dict()
        params.pop('csrfmiddlewaretoken')
        user = jsonpickle.loads(request.session.get('user'))
        Address.objects.create(userinfo=user, isdefault=(lambda count: True if count == 0 else False)(user.address_set.count()), **params)
        return HttpResponseRedirect('/user/address/')


def LoadAddr(request):
    pid = request.GET.get('pid', -1)
    pid = int(pid)
    arealist = Area.objects.filter(parentid=pid)

    # 手动构建响应格式
    jarealist = [{'id': area.pk, 'name': area.areaname} for area in arealist]

    return JsonResponse({'jareaList': jarealist})

class SetDefaultAddressView(View):
    def post(self, request):
        address_id = request.POST.get('address_id')
        user = jsonpickle.loads(request.session.get('user'))

        try:
            address = Address.objects.get(id=address_id, userinfo=user)
            # 将所有地址的默认状态设为False
            Address.objects.filter(userinfo=user).update(isdefault=False)
            # 将选中的地址设为默认
            address.isdefault = True
            address.save()
            return JsonResponse({'success': True})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'})
class DeleteAddressView(View):
    def post(self, request):
        address_id = request.POST.get('address_id')
        user = jsonpickle.loads(request.session.get('user'))
        try:
            address = Address.objects.get(id=address_id, userinfo=user)
            address.delete()
            return JsonResponse({'success': True})
        except Address.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Address not found'})