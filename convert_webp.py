#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png"}

def convert_image_to_webp(src_path: Path, dst_path: Path, quality: int = 85):
    """Convert a single image to WebP format."""
    try:
        with Image.open(src_path) as img:
            img.save(dst_path, format="WEBP", quality=quality)
        print(f"[OK] {src_path} -> {dst_path}")
    except Exception as e:
        print(f"[ERROR] Failed to convert {src_path}: {e}")

def batch_convert(input_dir: Path, output_dir: Path, quality: int):
    """Batch convert all supported images in a folder recursively."""
    if not input_dir.exists():
        print(f"[ERROR] Input directory does not exist: {input_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Traverse all files recursively
    for src_path in input_dir.rglob("*"):
        if src_path.suffix.lower() in SUPPORTED_EXTS:
            # Rebuild directory structure in output folder
            relative = src_path.relative_to(input_dir)
            dst_path = (output_dir / relative).with_suffix(".webp")
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Skip existing webp files
            if dst_path.exists():
                print(f"[SKIP] Already exists: {dst_path}")
                continue

            convert_image_to_webp(src_path, dst_path, quality)

def main():
    parser = argparse.ArgumentParser(
        description="Batch convert JPG/PNG images to WebP format."
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Path to the input folder containing images."
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Path to the output folder to save WebP images."
    )
    parser.add_argument(
        "--quality", "-q", type=int, default=85,
        help="WebP quality (0-100, default: 85)."
    )

    args = parser.parse_args()

    batch_convert(
        input_dir=Path(args.input),
        output_dir=Path(args.output),
        quality=args.quality
    )

if __name__ == "__main__":
    main()