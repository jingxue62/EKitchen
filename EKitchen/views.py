from django.http import HttpResponse
from django.http import JsonResponse

from .models import User, Product, Order

from django.core import serializers
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
    response = "Product id = %s."
    return HttpResponse(response % pid)


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
    return JsonResponse({'data': list(Product.objects.values().order_by('-updated_at', '-rate', 'discount')[:num]), 'message': ""}, safe=False)


def get_product_search(request, keyword):
    return JsonResponse({'data': list(Product.objects.values().filter(description__contains=keyword)), 'message': ""}, safe=False)

# def get_product_description_contains(request, text):
#     # Elastic Search
#     return