from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db import connection
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from imagekit.cachefiles import ImageCacheFile
from imagekit.cachefiles.namers import source_name_as_path

from . import models
import random
from django.db.models import Prefetch
from django.db.models import Max

from .imagegenerators import ThumbnailList

storage = get_storage_class()()


# Create your views here.


def index(request):
    return render(request, "shop/index.jinja2")


def view_product(request, product_id: int):
    product = get_object_or_404(models.Product.objects.all().prefetch_related('design', 'product_type', 'pictures'),
                                pk=product_id)
    images = product.pictures.all()
    image = images[0]

    # Get random products that don't use the same design or the same product type
    pks = list(models.Product.objects
               .exclude(design=product.design)
               .exclude(product_type=product.product_type)
               .values_list('pk', flat=True))
    random_ids = random.sample(pks, 4)
    random_products = models.Product.objects \
        .filter(pk__in=random_ids) \
        .select_related('design', 'product_type') \
        .prefetch_related('pictures') \
        .all()

    return render(request, "shop/product.jinja2", {"product": product,
                                                   "images": images,
                                                   "image": image,
                                                   "random_products": random_products})


def view_product_type(request, pk: int):
    product_type = get_object_or_404(models.ProductType.objects.all(),
                                     pk=pk)
    products = product_type.products.all().prefetch_related('product_type', 'design', 'pictures').order_by(
        '-print_location', '?')

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


def get_designs():
    designs = []
    designs_sql = """
        SELECT
            design_name,
            design_id,
            shop_product_id,
            photo AS photo_url
        FROM
            shop_productpicture
            INNER JOIN (
                SELECT
                    name AS design_name,
                    id AS design_id,
                    shop_product_id
                FROM
                    shop_design
                    INNER JOIN (
                        SELECT
                            design_id,
                            MAX(shop_product.id) AS shop_product_id
                        FROM
                            shop_product
                        GROUP BY
                            shop_product.design_id) AS sqy ON shop_design.id = sqy.design_id) AS sqyy ON shop_productpicture.product_id = sqyy.shop_product_id
        WHERE
            shop_productpicture.is_main_image = TRUE;
    """

    with connection.cursor() as cursor:
        cursor.execute(designs_sql)
        desc = [d[0] for d in cursor.description]
        all_data = cursor.fetchall()

    for design_data in all_data:
        fieldsdict = {k: v for k, v in zip(desc, design_data)}
        photo_url = fieldsdict['photo_url']
        fieldsdict['photo'] = models.ProductPicture(photo=photo_url).thumbnail_list

        designs.append(fieldsdict)
    return designs


designs = get_designs()


def view_designs(request):
    return render(request, "shop/designs.jinja2", {"designs": designs, })


def get_product_types():
    product_types = []
    product_types_sql = """
        SELECT
            product_type_name,
            product_type_id,
            shop_product_id,
            photo AS photo_url
        FROM
            shop_productpicture
            INNER JOIN (
                SELECT
                    name AS product_type_name,
                    id AS product_type_id,
                    shop_product_id
                FROM
                    shop_producttype
                    INNER JOIN (
                        SELECT
                            product_type_id,
                            MAX(shop_product.id) AS shop_product_id
                        FROM
                            shop_product
                        GROUP BY
                            shop_product.product_type_id) AS sqy ON shop_producttype.id = sqy.product_type_id) AS sqyy 
                            ON shop_productpicture.product_id = sqyy.shop_product_id
        WHERE
            shop_productpicture.is_main_image = TRUE;
    """

    with connection.cursor() as cursor:
        cursor.execute(product_types_sql)
        desc = [d[0] for d in cursor.description]
        all_data = cursor.fetchall()

    for design_data in all_data:
        fieldsdict = {k: v for k, v in zip(desc, design_data)}
        photo_url = fieldsdict['photo_url']
        photo = models.ProductPicture(photo=photo_url).thumbnail_list
        fieldsdict['photo'] = photo
        fieldsdict['photo_url'] = photo.url
        fieldsdict['photo_width'] = photo.width
        fieldsdict['photo_height'] = photo.height
        fieldsdict['view_more_url'] = reverse('shop_product_type_info', kwargs={'pk': fieldsdict['product_type_id']})

        product_types.append(fieldsdict)
    return product_types


product_types = get_product_types()


def view_product_types(request):
    return render(request, "shop/product_types.jinja2", {"product_types": product_types, })


def product_api(request, product_id: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    product = get_object_or_404(models.Product.objects.all().prefetch_related('design', 'product_type', 'pictures'),
                                pk=product_id)
    return HttpResponseRedirect(product.external_url)
