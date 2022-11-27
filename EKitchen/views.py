from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from .models import User, Product, Order

from django.core import serializers
from django.conf import settings
from django.db.models import Q
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
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
    user_info = User.objects.filter(id=prod.get('owner_id')).values()[0]
    prod.update(user_info)
    return JsonResponse({'data': prod, 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_order(request, oid):
    return HttpResponse("Order id = %s." % oid)


@cache_page(CACHE_TTL)
def get_all_users(request):
    return JsonResponse({'data': list(User.objects.values()), 'message': ""}, safe=False)


@cache_page(CACHE_TTL)
def get_sorted_products(query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()] 
    cursor.connection.close()
    return result


@cache_page(CACHE_TTL)
def get_all_products(request, num):
    query1 = '''select EKitchen_product.price * EKitchen_product.discount as realPrice, 
                                    EKitchen_product.*, EKitchen_user.username
                            from EKitchen_product, EKitchen_user 
                            where EKitchen_product.owner_id = EKitchen_user.id
                            order by EKitchen_product.updated_at DESC'''

    query2 = '''select EKitchen_product.price * EKitchen_product.discount as realPrice, 
                                    EKitchen_product.*, EKitchen_user.username
                            from EKitchen_product, EKitchen_user 
                            where EKitchen_product.owner_id = EKitchen_user.id
                            order by realPrice ASC'''
    query3 = '''select EKitchen_product.price * EKitchen_product.discount as realPrice, 
                                    EKitchen_product.*, EKitchen_user.username
                            from EKitchen_product, EKitchen_user 
                            where EKitchen_product.owner_id = EKitchen_user.id
                            order by realPrice DESC'''
    if num == 2:
        result = get_sorted_products(query2)
        return JsonResponse({'data': result, 'message': ""}, safe=False)
    elif num == 3:
        result = get_sorted_products(query3)
        return JsonResponse({'data': result, 'message': ""}, safe=False)
    else:
        result = get_sorted_products(query1)
        return JsonResponse({'data': result, 'message': ""}, safe=False)

# @cache_page(CACHE_TTL)
# def get_all_products(request):
#     return JsonResponse({'data': list(Product.objects.values()), 'message': ""}, safe=False)


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
