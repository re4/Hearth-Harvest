"""Convert the approved concept sheet into crisp 16px production sprites."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "art/source-item-sheet-v2.png"
TEXTURES = ROOT / "src/main/resources/assets/hearth_and_harvest/textures"
COLS = 8
ROWS = 4
MAX_SPRITE_EXTENT = 12
NAMES = [
    "tomato", "onion", "cucumber", "corn", "bell_pepper", "strawberry", "rice", "spinach",
    "tomato_seeds", "onion_seeds", "cucumber_seeds", "corn_seeds", "bell_pepper_seeds", "strawberry_seeds", "rice_seeds", "spinach_seeds",
    "flour", "cooking_oil", "dough", "cheese", "toast", "garden_salad", "tomato_soup", "veggie_stew",
    "stuffed_pepper", "strawberry_tart", "corn_chowder", "fried_rice", "farmers_breakfast", "cutting_board", "cooking_pot", "market_crate",
]


def is_key(pixel):
    r, g, b, _ = pixel
    return r > 205 and b > 175 and g < 80 and abs(r - b) < 80


def occupied_bands(values):
    bands = []
    for value in values:
        if not bands or value > bands[-1][1] + 1:
            bands.append([value, value])
        else:
            bands[-1][1] = value
    return bands


def content_bands(image, axis):
    if axis == "x":
        values = [
            x for x in range(image.width)
            if any(not is_key(image.getpixel((x, y))) for y in range(image.height))
        ]
    else:
        values = [
            y for y in range(image.height)
            if any(not is_key(image.getpixel((x, y))) for x in range(image.width))
        ]
    return occupied_bands(values)


def safe_bounds(bands, extent):
    """Place crop boundaries in the empty gaps between painted rows/columns."""
    return [0, *[(left[1] + right[0] + 1) // 2 for left, right in zip(bands, bands[1:])], extent]


def normalize_dark_chroma_edge(image):
    """Recolor dark purple key fringe from non-purple food/tool outlines."""
    candidates = set()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = image.getpixel((x, y))
            if not alpha or max(red, green, blue) > 100:
                continue
            if blue < red * 0.9 or blue < green * 1.2:
                continue
            neighbors = [
                (x + dx, y + dy)
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                if dx or dy
            ]
            if any(
                nx < 0 or ny < 0 or nx >= image.width or ny >= image.height
                or not image.getpixel((nx, ny))[3]
                for nx, ny in neighbors
            ):
                candidates.add((x, y))

    for x, y in candidates:
        replacements = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                point = (x + dx, y + dy)
                if dx == dy == 0 or point in candidates:
                    continue
                if 0 <= point[0] < image.width and 0 <= point[1] < image.height:
                    pixel = image.getpixel(point)
                    if pixel[3]:
                        replacements.append(pixel)
        if replacements:
            red, green, blue, _ = min(replacements, key=lambda pixel: sum(pixel[:3]))
            image.putpixel((x, y), (red, green, blue, 255))
    return image


sheet = Image.open(SOURCE).convert("RGBA")
x_bands = content_bands(sheet, "x")
y_bands = content_bands(sheet, "y")
if len(x_bands) != COLS or len(y_bands) != ROWS:
    raise RuntimeError(f"Expected an {COLS}x{ROWS} item layout, found {len(x_bands)}x{len(y_bands)}")
x_bounds = safe_bounds(x_bands, sheet.width)
y_bounds = safe_bounds(y_bands, sheet.height)

# Key the backdrop once on the complete sheet. The safe row/column bounds below
# are derived from the actual artwork gaps, so no item is exposed to a crop edge.
pixels = sheet.load()
for y in range(sheet.height):
    for x in range(sheet.width):
        if is_key(pixels[x, y]):
            pixels[x, y] = (0, 0, 0, 0)

for index, name in enumerate(NAMES):
    col, row = index % COLS, index // COLS
    box = (x_bounds[col], y_bounds[row], x_bounds[col + 1], y_bounds[row + 1])
    cell = sheet.crop(box)
    alpha_box = cell.getchannel("A").getbbox()
    if alpha_box is None:
        raise RuntimeError(f"No sprite found for {name}")
    if alpha_box[0] == 0 or alpha_box[1] == 0 or alpha_box[2] == cell.width or alpha_box[3] == cell.height:
        raise RuntimeError(f"Source artwork for {name} touches its extraction boundary")
    sprite = cell.crop(alpha_box)
    scale = min(MAX_SPRITE_EXTENT / sprite.width, MAX_SPRITE_EXTENT / sprite.height)
    target = (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale)))
    sprite = sprite.resize(target, Image.Resampling.LANCZOS)

    # Collapse the painted source to a hard-edged, limited pixel palette.
    alpha = sprite.getchannel("A").point(lambda a: 255 if a >= 96 else 0)
    rgb = sprite.convert("RGB").quantize(colors=14, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    out = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    out.alpha_composite(rgb, ((16 - rgb.width) // 2, (16 - rgb.height) // 2))
    if index >= 16:
        out = normalize_dark_chroma_edge(out)
    # Seed packets are owned by generate_expanded_content.py, where every one
    # receives its matching miniature crop icon. Do not replace them with the
    # old loose-seed drawings when this source sheet is re-imported.
    if not name.endswith("_seeds"):
        out.save(TEXTURES / "item" / f"{name}.png")

icon = Image.open(TEXTURES / "item/tomato.png").resize((128, 128), Image.Resampling.NEAREST)
icon.save(TEXTURES.parent / "icon.png")
