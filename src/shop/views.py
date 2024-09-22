
from django.core.cache import cache
from django.db import connection
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from . import models
import random


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


def get_productype_products(product_type_id):
    key = f'get_productype_products-{product_type_id}'

    products = cache.get(key, default=[])
    if len(products):
        return products

    sql = """
    SELECT
    "shop_product"."id" as "product_id",
    "shop_product"."name" as "product_name",
    "shop_product"."print_location" as "product_print_location",
    "shop_product"."color_product_name" as "product_color_product_name",
    "shop_product"."price" as "product_price",
    "shop_design"."name" as "design_name",
    "shop_productpicture"."photo" as "product_photo_url"
    FROM
    "shop_product"
    INNER JOIN "shop_design" ON ("shop_product"."design_id" = "shop_design"."id")
    INNER JOIN (
        SELECT
            "shop_productpicture"."photo",
            "shop_productpicture"."product_id"
        FROM
            "shop_productpicture"
        WHERE
            "shop_productpicture"."is_main_image" = TRUE
    ) AS "shop_productpicture" ON ("shop_product"."id" = "shop_productpicture"."product_id")
    
    WHERE
    "shop_product"."product_type_id" = %s
    ORDER BY
    "shop_product"."print_location" DESC,
    RANDOM()
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [product_type_id])
        desc = [d[0] for d in cursor.description]
        all_data = cursor.fetchall()

    for product_data in all_data:
        fieldsdict = {k: v for k, v in zip(desc, product_data)}

        photo_url = fieldsdict['product_photo_url']

        photo = models.ProductPicture(photo=photo_url).thumbnail_list

        fieldsdict['photo'] = photo

        fieldsdict['photo_url'] = photo.url
        fieldsdict['photo_width'] = photo.width
        fieldsdict['photo_height'] = photo.height

        name = fieldsdict['design_name']
        color = fieldsdict["product_color_product_name"].replace(fieldsdict["product_name"], '', 1).strip()
        print_location = fieldsdict["product_print_location"]
        if print_location == "back" and color:
            name += f" ({color}, {print_location} printed)"
        elif print_location == "back":
            name += f", {print_location} printed"
        elif color:
            name += f" ({color})"

        fieldsdict['product_full_name'] = name

        products.append(fieldsdict)

    cache.set(key, products, 86400)

    return products


def view_product_type(request, pk: int):
    product_type = get_object_or_404(models.ProductType,
                                     pk=pk)

    products = get_productype_products(pk)

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
        photo = models.ProductPicture(photo=photo_url).thumbnail_list
        fieldsdict['photo'] = photo
        fieldsdict['photo_url'] = photo.url
        fieldsdict['photo_width'] = photo.width
        fieldsdict['photo_height'] = photo.height
        designs.append(fieldsdict)
    return designs


try:
    designs = get_designs()
except:
    designs = []


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
