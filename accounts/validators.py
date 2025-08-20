from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions_list = [".png", ".jpeg", ".jpg"]
    if not ext.lower() in valid_extensions_list:
        ext_str = ",".join(valid_extensions_list)
        raise ValidationError(f"Unsupported File Extension Allow only ({ext_str}) files")