import json
import pathlib

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from shop.models import Product, ProductPicture, ProductType, Design


class Command(BaseCommand):
    help = 'Import data from redbubble scraping'

    def add_arguments(self, parser):
        parser.add_argument('redbubble_data_root', type=pathlib.Path)

    @transaction.atomic
    def handle(self, *args, **options):
        base_path: pathlib.Path = options['redbubble_data_root']

        for design_dir in [x for x in base_path.iterdir() if x.is_dir()]:
            design_name = design_dir.name
            design, _ = Design.objects.get_or_create(name=design_name)

            self.stdout.write(f'Importing {design}')

            for product_dir in [x for x in design_dir.iterdir() if x.is_dir()]:
                product_name = product_dir.name.replace(design_name, "", 1).strip()

                product_type, _ = ProductType.objects.get_or_create(name=product_name)
                self.stdout.write(f'Importing {design}/{product_type}')

                download_info_path = product_dir / "download.json"
                try:
                    with open(download_info_path, "r") as f:
                        download_info = json.load(f)
                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(f'No data found for {download_info_path}'))

                features_html = download_info["features_html"]
                varients = download_info["varients"]

                for varient in varients:
                    product = Product(
                        name=product_dir.name,
                        html_description=features_html,
                        external_url=varient["url"],

                        design=design,
                        product_type=product_type,

                        sizes_names=varient["sizes_names"],
                        price=varient["price"],
                        print_location=varient["print_location_text"] or "",
                        color_product_name=varient["color_product_name"] or "")

                    product.save()
                    for image_data in varient["images"]:
                        image_rel_path = image_data["link"]
                        image_path = base_path / image_rel_path.replace("redbubble/", "", 1)

                        with open(image_path, "rb") as image_file:
                            image = ProductPicture(product=product,
                                                   is_main_image=image_data["main"],
                                                   photo=File(image_file))

                            image.save()

            self.stdout.write(self.style.SUCCESS(f'Imported {design_name}'))
