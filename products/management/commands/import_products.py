import json
import logging
import os

from django.core.files import File
from django.core.management.base import BaseCommand

from products.models import (
    Product,
    ProductVariant,
)  # Adjust import based on your app name

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import products from JSON file and create Product and ProductVariant models"

    def add_arguments(self, parser):
        parser.add_argument("base_path", type=str, help="Base path for JSON and assets")

    def handle(self, *args, **options):
        base_path = options["base_path"]
        json_path = os.path.join(base_path, "products-to-import.json")
        if not os.path.exists(json_path):
            logger.error(f"JSON file not found: {json_path}")
            self.stdout.write(self.style.ERROR(f"JSON file not found: {json_path}"))
            return

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                products_data = json.load(f)
            logger.info(f"Loaded {len(products_data)} products from {json_path}")
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            self.stdout.write(self.style.ERROR("Failed to load JSON file"))
            return

        imported_count = 0
        skipped_count = 0
        for data in products_data:
            original_title = data.get("title", "Untitled")
            clean_title = data.get("clean_title")
            if not clean_title:
                logger.warning(
                    f"Skipping product without clean_title: {original_title}"
                )
                skipped_count += 1
                continue

            local_image_path = data.get("local_image_path")
            full_image_path = os.path.join(base_path, local_image_path)
            if not local_image_path or not os.path.exists(full_image_path):
                logger.warning(
                    f"Skipping product without valid image path: {original_title}"
                )
                skipped_count += 1
                continue

            try:
                product = Product(title=clean_title)
                with open(full_image_path, "rb") as img_file:
                    product.image.save(
                        os.path.basename(full_image_path), File(img_file)
                    )
                product.save()
                logger.info(f"Created Product: {clean_title}")

                sku = data.get("sku", "")
                height = data.get("height_cm", 0.00)
                width = data.get("width_cm", 0.00)
                length = data.get("depth_cm", 0.00)
                external_url = data.get("product_page_url", "")

                variant = ProductVariant(
                    product=product,
                    sku=sku,
                    height=height,
                    width=width,
                    length=length,
                    stock_quantity=0,
                    color="",
                    external_url=external_url,
                    regular_price=1.99,
                )
                with open(full_image_path, "rb") as img_file:
                    variant.image.save(
                        os.path.basename(full_image_path), File(img_file)
                    )
                variant.save()
                logger.info(f"Created ProductVariant for SKU: {sku}")

                imported_count += 1
                self.stdout.write(self.style.SUCCESS(f"Imported {clean_title}"))

            except Exception as e:
                logger.error(f"Error importing product {original_title}: {e}")
                self.stdout.write(
                    self.style.ERROR(f"Error importing {original_title}: {str(e)}")
                )
                skipped_count += 1

        logger.info(
            f"Import completed. Imported: {imported_count}, Skipped/Errored: {skipped_count}"
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed. Imported: {imported_count}, Skipped/Errored: {skipped_count}"
            )
        )
