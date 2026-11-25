from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_size(image):

    max_size = 5 * 1024 * 1024

    if image.size > max_size:

        raise ValidationError(
            "حجم تصویر نباید بیشتر از ۵ مگابایت باشد."
        )


def validate_image_extension(image):

    allowed_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    file_name = image.name.lower()

    if not file_name.endswith(allowed_extensions):

        raise ValidationError(
            "فرمت تصویر باید JPG، JPEG، PNG یا WEBP باشد."
        )


def validate_image_content(image):

    try:

        image_file = Image.open(image)

        image_file.verify()

    except Exception:

        raise ValidationError(
            "فایل انتخاب شده یک تصویر معتبر نیست."
        )

    finally:

        image.seek(0)