from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from .models import User, Product, Order

from django.core import serializers
from django.conf import settings
from django.db.models import Q
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

import json

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def get_user(request, uid):
    # check cache
    result = serializers.serialize('json', [User.objects.get(pk=uid), ])
    # return HttpResponse("User id = %s." % uid)
    # return serializers.serialize('json', [data, ])
    data = json.loads(result)
    data = json.dumps(data[0])
    return HttpResponse(data, content_type='application/json')


@cache_page(CACHE_TTL)
def get_product(request, pid):
    prod = Product.objects.filter(id=pid).values()[0]
    user_info = User.objects.filter(id=prod.get('owner_id')).values('username','address', 'email', 'is_active')[0]
    prod.update(user_info)
    return JsonResponse({'data': prod, 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_order(request, oid):
    return HttpResponse("Order id = %s." % oid)


@cache_page(CACHE_TTL)
def get_all_users(request):
    return JsonResponse({'data': list(User.objects.values()), 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_all_products(request):
    results = []
    product_list = Product.objects.values()
    # Enrich data
    for o in product_list:
        user_obj = User.objects.filter(id=o.get('owner_id')).values()[0]
        o['username'] = user_obj['username']
        o['realPrice'] = o['price']*o['discount']
        results.append(o)
    return JsonResponse(
        {'data': results, 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_all_orders(request):
    return JsonResponse({'data': list(Order.objects.values()), 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_top_products(request, num):
    return JsonResponse({'data': list(Product.objects.values().order_by('-rate')[:num]), 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_recommend_products(request, num):
    return JsonResponse({'data': list(Product.objects.order_by('-updated_at', '-rate', 'discount').values()[:num]), 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_product_search(request, keywords):
    kw = keywords.split(';')
    user_ids = [i.get('id') for i in User.objects.filter(username__in=kw).values()]
    results = []
    hs = set()
    for item in kw:
        plist = Product.objects.filter(Q(description__contains=item) | Q(name__contains=item)).values()
        hs |= set([i.get('id') for i in plist if i])
        results += plist
    if user_ids:
        results += [p for p in Product.objects.filter(owner_id__in=user_ids).values() if p.get('id') not in hs]
    return JsonResponse({'data': results, 'message': ""}, safe=False)

@cache_page(CACHE_TTL)
def get_orders_by_user(request, userId):
    results = []
    order_list = Order.objects.filter(buyer=userId).values()
    # Enrich data
    for o in order_list:
        product_obj = Product.objects.filter(id=o.get('product_id')).values()[0]
        o['name'] = product_obj['name']
        o['image'] = product_obj['image']
        o['price'] = product_obj['price']
        o['discount'] = product_obj['discount']
        o['owner_id'] = product_obj['owner_id']
        o['is_active'] = product_obj['is_active']
        o['availability'] = product_obj['availability']
        user_obj = User.objects.filter(id=product_obj.get('owner_id')).values()[0]
        o['username'] = user_obj['username']
        results.append(o)
    return JsonResponse(
        {'data': results, 'message': ""}, safe=False)


@csrf_exempt
def place_order(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            product_instance = Product.objects.get(id=body["product_id"])
            user_instance = User.objects.get(id=body["buyer_id"])
            new_order = Order(product=product_instance,
                              buyer=user_instance,
                              quantity=body["quantity"],
                              description=body["desc"])
            new_order.save()
        else:
            raise Exception("Please post data to this interface.")
    except Exception as err:
        return JsonResponse({'data': '', 'message': "Error:" + str(err)}, safe=False)
    return JsonResponse({'data': '', 'message': "Successfully done."}, safe=False)


@csrf_exempt
def delete_order(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print("deleting an order:",body["id"] )
            order_instance = Order.objects.get(id=body["id"])
            print("deleting an order:", order_instance)
            order_instance.delete()
        else:
            raise Exception("Please post Order ID to this interface.")
    except Exception as err:
        raise
        # return JsonResponse({'data': '', 'message': "Error:" + str(err)}, safe=False)
    return JsonResponse({'data': '', 'message': "Successfully done."}, safe=False)

@csrf_exempt
def register(request):
    try:
        if request.method == 'POST':
            print("registering...")
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            print("Register post body:", body)
            print("Register email:", body["email"])
            print("Register username:", body["username"])
            user_email = [i.get('email') for i in User.objects.filter(email=body["email"]).values()]
            user_name = [i.get('username') for i in User.objects.filter(username=body["username"]).values()]
            if (len(user_email) != 0 ):
                return JsonResponse({'data': '', 'message': "Error: The email is existed! "}, safe=False)
            elif (len(user_name) != 0 ):
                return JsonResponse({'data': '', 'message': "Error: The username is existed! "}, safe=False)
            else:
                new_user = User(email=body["email"],
                                username=body["username"],
                                password=body["password"],
                                first = '',
                                last ='',
                                address='')  
                new_user.save()
        else:
            raise Exception("Please post data to this interface.")
    except Exception as err:
        return JsonResponse({'data': '', 'message': "Error:" + str(err)}, safe=False)
    return JsonResponse({'data': '', 'message': "Successfully done."}, safe=False)

@csrf_exempt
def signin(request):
    try:
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            user_by_email = User.objects.filter(email=body["email"]).values()[0]
            if (user_by_email):
                if user_by_email["password"] == body["password"]:
                    # print("matched!")
                    return JsonResponse({'data': user_by_email, 'message': ""}, safe=False)
                else:
                    # print("not matched!")
                    return JsonResponse({'data': '', 'message': "Error: The email and password are not matched."}, safe=False)
            else:
                # print("The email is not existed!")
                return JsonResponse({'data': '', 'message': "Error: The email is not existed."}, safe=False)
        else:
            raise Exception("Please post data to this interface.")
    except Exception as err:
        # print("Exception errors!")
        return JsonResponse({'data': '', 'message': "Error:" + str(err)}, safe=False)

# @cache_page(CACHE_TTL)
def get_kitchens_by_user(request, userId):
    results = []
    product_list = Product.objects.filter(owner=userId).values()
    # Enrich data
    for p in product_list:
        order_list = list(Order.objects.filter(product=p.get('id')).values())
        p['order_num'] = len(order_list)
        results.append(p)
    return JsonResponse(
        {'data': results, 'message': ""}, safe=False)

# @cache_page(CACHE_TTL)
def get_kitchens_by_order(request, userId):
    results = []
    product_list = Product.objects.filter(owner=userId).values()
    # Enrich data
    for p in product_list:
        order_list = Order.objects.filter(product=p.get('id')).values()
        print("order_list:", order_list)
        for o in order_list:
            print("order_obj:", o)
            o['name'] = p['name']
            o['image'] = p['image']
            o['price'] = p['price']
            o['discount'] = p['discount']
            o['owner_id'] = p['owner_id']
            o['is_active'] = p['is_active']
            o['availability'] = p['availability']
            user_obj = User.objects.filter(id=userId).values()[0]
            o['username'] = user_obj['username']
            results.append(o)
    print("user orders:", results)
    results.append(o)
    return JsonResponse(
        {'data': results, 'message': ""}, safe=False)
