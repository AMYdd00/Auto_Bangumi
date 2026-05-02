import hashlib
import os
import re


def _sanitize_filename(name: str) -> str:
    """Remove or replace characters that are invalid in filenames."""
    # Replace invalid filename characters with underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", name)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")
    # Truncate to reasonable length
    return sanitized[:100]


def save_image(img, suffix, bangumi_name: str = ""):
    if bangumi_name:
        # Use bangumi name as filename for easy lookup
        safe_name = _sanitize_filename(bangumi_name)
        image_path = f"data/posters/{safe_name}.{suffix}"
        # Avoid overwriting if file already exists with different content
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                if f.read() == img:
                    return f"posters/{safe_name}.{suffix}"
        with open(image_path, "wb") as f:
            f.write(img)
        return f"posters/{safe_name}.{suffix}"
    else:
        # Fall back to hash-based name
        img_hash = hashlib.md5(img).hexdigest()[0:8]
        image_path = f"data/posters/{img_hash}.{suffix}"
        with open(image_path, "wb") as f:
            f.write(img)
        return f"posters/{img_hash}.{suffix}"


def load_image(img_path):
    if img_path:
        with open(f"data/{img_path}", "rb") as f:
            return f.read()
    else:
        return None
