from io import BytesIO

from PIL import Image, ImageOps
from django.core.files.base import ContentFile


MAX_IMAGE_SIZE = (2400, 2400)


def optimize_image(image_field):

    image = Image.open(image_field)

    image = ImageOps.exif_transpose(image)

    original_format = image.format

    image.thumbnail(
        MAX_IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    output = BytesIO()

    if original_format == "PNG":

        image.save(
            output,
            format="PNG",
            optimize=True
        )

    elif original_format == "WEBP":

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        image.save(
            output,
            format="WEBP",
            quality=85,
            method=6
        )

    else:

        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(
            output,
            format="JPEG",
            quality=85,
            optimize=True
        )

    output.seek(0)

    return ContentFile(
        output.read()
    )