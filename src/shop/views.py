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
                                                   "images": images,
                                                   "image": image})

