import random
import string

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Design(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    html_description = models.TextField()
    external_url = models.URLField()

    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    sizes_names = models.JSONField(default=list)
    price = models.CharField(max_length=10)
    print_location = models.CharField(choices=(("front", "Front"), ("back", "Back")), blank=True, max_length=10)
    color_product_name = models.CharField(max_length=600, blank=True)

    def get_parsed_price(self) -> float:
        return float(self.price.replace("$", "").replace(",", "."))

    def get_margin(self) -> float:
        return round(self.get_parsed_price() * 0.2, 2)

    @property
    def color(self):
        return self.color_product_name.replace(self.product_type.name, '', 1).strip()

    @property
    def display_name(self):
        if self.color_product_name:
            name =  f"{self.design} {self.color_product_name}"
        else:
            name = self.name

        if self.print_location:
            name += f" ({self.print_location} printed)"

        return name

    def __str__(self):
        return self.display_name


def make_filepath(instance, filename):
    """
    Produces a unique file path for the upload_to of a FileField.
    """
    product_type = instance.product.product_type.name.replace(' ', '-')
    product_name = instance.product.display_name.replace(' ', '-')
    random_string1 = ''.join(random.sample(string.ascii_letters, k=3))
    random_string2 = ''.join(random.sample(string.ascii_letters, k=3))
    extension = filename.split('.')[-1]

    new_filename = f"{random_string1}-{product_name}-{random_string2}.{extension}"

    return '/'.join([instance.__class__.__name__.lower(), product_type, new_filename])


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pictures")
    photo = models.ImageField(upload_to=make_filepath, unique=True)
