from django.http import HttpResponse
from django.http import JsonResponse

from .models import User, Product, Order

from django.core import serializers
from django.db.models import Q
import json


def get_user(request, uid):
    # check cache
    result = serializers.serialize('json', [User.objects.get(pk=uid), ])
    # return HttpResponse("User id = %s." % uid)
    # return serializers.serialize('json', [data, ])
    data = json.loads(result)
    data = json.dumps(data[0])
    return HttpResponse(data, content_type='application/json')


def get_product(request, pid):
    prod = Product.objects.filter(id=pid).values()[0]
    user_info = User.objects.filter(id=prod.get('owner_id')).values()[0]
    prod.update(user_info)
    return JsonResponse({'data': prod, 'message': ""}, safe=False)


def get_order(request, oid):
    return HttpResponse("Order id = %s." % oid)


def get_all_users(request):
    return JsonResponse({'data': list(User.objects.values()), 'message': ""}, safe=False)


def get_all_products(request):
    return JsonResponse({'data': list(Product.objects.values()), 'message': ""}, safe=False)


def get_all_orders(request):
    return JsonResponse({'data': list(Order.objects.values()), 'message': ""}, safe=False)


def get_top_products(request, num):
    return JsonResponse({'data': list(Product.objects.values().order_by('-rate')[:num]), 'message': ""}, safe=False)


def get_recommend_products(request, num):
    return JsonResponse({'data': list(Product.objects.order_by('-updated_at', '-rate', 'discount').values()[:num]), 'message': ""}, safe=False)


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


# def get_product_description_contains(request, text):
#     # Elastic Search
#     return