from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from . import models


# Create your views here.


def index(request):
    return render(request, "shop/index.jinja2")


def view_product(request, product_id: int):
    product = get_object_or_404(models.Product.objects.all().prefetch_related('design', 'product_type', 'pictures'),
                                pk=product_id)
    images = product.pictures.all()
    image = images[0]

    return render(request, "shop/product.jinja2", {"product": product,
                                                   "images" : images,
                                                   "image"  : image})


def view_product_type(request, pk: int):
    product_type = get_object_or_404(models.ProductType.objects.all(),
                                     pk=pk)
    products = product_type.products.all().prefetch_related('product_type', 'design', 'pictures').order_by('-print_location', '?')

    return render(request, "shop/product_type.jinja2", {"category": product_type,
                                                        "products": products,
                                                        })


def view_design(request, pk: int):
    design = get_object_or_404(models.Design.objects.all(),
                               pk=pk)
    products = design.products.all().prefetch_related('product_type', 'design', 'pictures').order_by('?')

    return render(request, "shop/design.jinja2", {"category": design,
                                                  "products": products,
                                                  })


def product_api(request, product_id: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    product = get_object_or_404(models.Product.objects.all().prefetch_related('design', 'product_type', 'pictures'),
                                pk=product_id)
    return HttpResponseRedirect(product.external_url)
