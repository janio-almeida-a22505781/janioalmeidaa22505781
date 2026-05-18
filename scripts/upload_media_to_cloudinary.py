#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

import django
from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.db.models.fields.files import FileField, ImageField

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.chdir(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

MEDIA_ROOT = Path(settings.MEDIA_ROOT)


def is_local_media_file(field_file):
    if not field_file:
        return False

    try:
        field_path = field_file.path
    except (NotImplementedError, ValueError, OSError):
        field_path = None

    if field_path and os.path.exists(field_path):
        return True

    # Some storage backends do not expose .path, so resolve via MEDIA_ROOT
    if field_file.name:
        local_path = MEDIA_ROOT / field_file.name
        return local_path.exists()

    return False


def upload_file_field(obj, field, dry_run=False):
    field_file = getattr(obj, field.name)
    if not field_file:
        return False

    if not is_local_media_file(field_file):
        return False

    local_path = MEDIA_ROOT / field_file.name
    if not local_path.exists():
        return False

    if dry_run:
        print(f"[dry-run] would upload {obj.__class__.__name__}.{field.name} for {obj}")
        return True

    with open(local_path, "rb") as f:
        django_file = File(f)
        field_file.save(os.path.basename(local_path), django_file, save=False)
    return True


def find_file_fields(app_label=None):
    for model in apps.get_models():
        if app_label and model._meta.app_label != app_label:
            continue

        file_fields = [f for f in model._meta.fields if isinstance(f, (FileField, ImageField))]
        if file_fields:
            yield model, file_fields


def main():
    parser = argparse.ArgumentParser(
        description="Upload local media/ files to Cloudinary by re-saving Django FileFields/ImageFields.")
    parser.add_argument(
        "--app",
        help="Limit processing to a single app label (for example 'portfolio').",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would be uploaded without changing anything.",
    )
    args = parser.parse_args()

    total_objects = 0
    total_uploaded = 0
    total_skipped = 0

    models_scanned = list(find_file_fields(app_label=args.app))
    for model, fields in models_scanned:
        print(f"Scanning model {model.__name__} ({model._meta.app_label}) for fields: {[f.name for f in fields]}")
        qs = model.objects.all().iterator()
        for obj in qs:
            total_objects += 1
            updated_fields = []
            for field in fields:
                if upload_file_field(obj, field, dry_run=args.dry_run):
                    updated_fields.append(field.name)
                    total_uploaded += 1
            if updated_fields and not args.dry_run:
                obj.save(update_fields=updated_fields)
            if not updated_fields:
                total_skipped += 1

    print("\nFinished.")
    print(f"Models scanned: {len(models_scanned)}")
    print(f"Objects visited: {total_objects}")
    print(f"Fields uploaded: {total_uploaded}")
    print(f"Objects skipped: {total_skipped}")


if __name__ == "__main__":
    main()
