
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------- CONFIGURATION ----------

BASE_DIR = Path(__file__).parent

TEMPLATE = BASE_DIR / "template.png"
NAME_FILE = BASE_DIR / "names.txt"
OUTPUT_DIR = BASE_DIR / "output"
FONT_DIR = BASE_DIR / "fonts"

# Set to a font filename in the fonts folder,
# or leave as None to use Times New Roman.
CUSTOM_FONT = None

FONT_SIZE = 32
TEXT_COLOR = "#222222"

# Position of the name on the certificate
# (x, y) is the center of the name.
NAME_POSITION = (405, 234)

# -----------------------------------


def get_font():
    """Load custom font or default Times New Roman."""

    if CUSTOM_FONT:
        font_path = FONT_DIR / CUSTOM_FONT
    else:
        # Use bundled Times New Roman if available.
        bundled_font = FONT_DIR / "Times New Roman.ttf"

        # Standard Windows Times New Roman location.
        windows_font = Path("C:/Windows/Fonts/times.ttf")

        if bundled_font.exists():
            font_path = bundled_font
        elif windows_font.exists():
            font_path = windows_font
        else:
            raise FileNotFoundError(
                "Times New Roman not found. "
                "Place its TTF file in the fonts folder."
            )

    if not font_path.exists():
        raise FileNotFoundError(f"Font not found: {font_path}")

    return ImageFont.truetype(str(font_path), FONT_SIZE)


def generate_certificate(name, font):
    """Create and save one certificate."""

    image = Image.open(TEMPLATE).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Center the name at the configured position.
    x, y = NAME_POSITION
    draw.text(
        (x, y),
        name,
        font=font,
        fill=TEXT_COLOR,
        anchor="mm"
    )

    # Create a safe filename.
    safe_name = "".join(
        c for c in name if c.isalnum() or c in (" ", "-", "_")
    ).strip()

    output_path = OUTPUT_DIR / f"{safe_name}.png"
    image.save(output_path, "PNG")

    return output_path


def main():
    # Check required input files.
    if not TEMPLATE.exists():
        raise FileNotFoundError("Certificate template not found.")

    if not NAME_FILE.exists():
        raise FileNotFoundError("Name list not found.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Read names, ignoring empty lines.
    names = [
        line.strip()
        for line in NAME_FILE.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]

    if not names:
        print("No names found in names.txt.")
        return

    font = get_font()

    for index, name in enumerate(names, start=1):
        output_path = generate_certificate(name, font)
        print(f"{index}/{len(names)} Generated: {output_path.name}")

    print(f"\nCompleted! Generated {len(names)} certificates.")


if __name__ == "__main__":
    main()
