import random
import string

from django.contrib.auth.models import User
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.
from shop.imagegenerators import ThumbnailMini, ThumbnailList


class Design(models.Model):
    name = models.CharField(max_length=300, unique=True)
    show_in_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=300, unique=True)
    show_in_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    html_description = models.TextField()
    external_url = models.URLField()

    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name="products")
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="products")

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
            name = f"{self.design} {self.color_product_name}"
        else:
            name = self.name

        if self.print_location:
            name += f" ({self.print_location} printed)"

        return name

    @property
    def display_name_on_product_type(self):
        name = str(self.design)

        if self.print_location == "back" and self.color:
            name += f" ({self.color}, {self.print_location} printed)"
        elif self.print_location == "back":
            name += f", {self.print_location} printed"
        elif self.color:
            name += f" ({self.color})"

        return name

    @property
    def display_name_on_design(self):
        name = str(self.product_type)

        if self.print_location and self.color:
            name += f" ({self.color}, {self.print_location} printed)"
        elif self.print_location:
            name += f", {self.print_location} printed"
        elif self.color:
            name += f" ({self.color})"

        return name

    def __str__(self):
        return self.display_name


def make_filepath(instance, filename):
    """
    Produces a unique file path for the upload_to of a FileField.
    """
    product_type = instance.product.product_type.name.replace(' ', '-').replace('&', '-').replace('---', '-')
    product_name = instance.product.display_name.replace(' ', '-')
    random_string1 = ''.join(random.sample(string.ascii_letters, k=2))
    random_string2 = ''.join(random.sample(string.ascii_letters, k=2))
    extension = filename.split('.')[-1]

    new_filename = f"{random_string1}-{product_name}-{random_string2}.{extension}"
    return '/'.join([instance.__class__.__name__.lower(), product_type, new_filename])


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pictures")
    is_main_image = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=make_filepath, unique=True)

    thumbnail_list = ImageSpecField(source='photo',
                                    id='shop:thumbnail_list')

    thumbnail_mini = ImageSpecField(source='photo',
                                    id='shop:thumbnail_mini'
                                    )

    class Meta:
        ordering = ["-is_main_image"]
