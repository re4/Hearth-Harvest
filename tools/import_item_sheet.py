"""Convert the approved concept sheet into crisp 16px production sprites."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "art/source-item-sheet-v2.png"
TEXTURES = ROOT / "src/main/resources/assets/hearth_and_harvest/textures"
NAMES = [
    "tomato", "onion", "cucumber", "corn", "bell_pepper", "strawberry", "rice", "spinach",
    "tomato_seeds", "onion_seeds", "cucumber_seeds", "corn_seeds", "bell_pepper_seeds", "strawberry_seeds", "rice_seeds", "spinach_seeds",
    "flour", "cooking_oil", "dough", "cheese", "toast", "garden_salad", "tomato_soup", "veggie_stew",
    "stuffed_pepper", "strawberry_tart", "corn_chowder", "fried_rice", "farmers_breakfast", "cutting_board", "cooking_pot", "market_crate",
]


def is_key(pixel):
    r, g, b, _ = pixel
    return r > 205 and b > 175 and g < 80 and abs(r - b) < 80


sheet = Image.open(SOURCE).convert("RGBA")
w, h = sheet.size
for index, name in enumerate(NAMES):
    col, row = index % 8, index // 8
    box = (round(col * w / 8), round(row * h / 4), round((col + 1) * w / 8), round((row + 1) * h / 4))
    cell = sheet.crop(box)
    pixels = cell.load()
    for y in range(cell.height):
        for x in range(cell.width):
            if is_key(pixels[x, y]):
                pixels[x, y] = (0, 0, 0, 0)

    alpha_box = cell.getchannel("A").getbbox()
    if alpha_box is None:
        raise RuntimeError(f"No sprite found for {name}")
    sprite = cell.crop(alpha_box)
    scale = min(14 / sprite.width, 14 / sprite.height)
    target = (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale)))
    sprite = sprite.resize(target, Image.Resampling.LANCZOS)

    # Collapse the painted source to a hard-edged, limited pixel palette.
    alpha = sprite.getchannel("A").point(lambda a: 255 if a >= 96 else 0)
    rgb = sprite.convert("RGB").quantize(colors=14, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    rgb.putalpha(alpha)
    out = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    out.alpha_composite(rgb, ((16 - rgb.width) // 2, (16 - rgb.height) // 2))

    # Image generation occasionally leaves a tiny detached shadow at the very
    # bottom of a cell. Remove only those low, small components; legitimate
    # multi-part seed clusters sit together in the upper portion of the icon.
    occupied = {(x, y) for y in range(16) for x in range(16) if out.getpixel((x, y))[3]}
    components = []
    while occupied:
        todo = [occupied.pop()]
        component = set(todo)
        while todo:
            x, y = todo.pop()
            for neighbor in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if neighbor in occupied:
                    occupied.remove(neighbor)
                    component.add(neighbor)
                    todo.append(neighbor)
        components.append(component)
    for component in components:
        if min(y for _, y in component) >= 12 and len(component) <= 12:
            for point in component:
                out.putpixel(point, (0, 0, 0, 0))

    clean_box = out.getchannel("A").getbbox()
    if clean_box:
        clean = out.crop(clean_box)
        scale = min(14 / clean.width, 14 / clean.height)
        size = (max(1, round(clean.width * scale)), max(1, round(clean.height * scale)))
        clean = clean.resize(size, Image.Resampling.NEAREST)
        out = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        out.alpha_composite(clean, ((16-clean.width)//2, (16-clean.height)//2))

    out.save(TEXTURES / "item" / f"{name}.png")

icon = Image.open(TEXTURES / "item/tomato.png").resize((128, 128), Image.Resampling.NEAREST)
icon.save(TEXTURES.parent / "icon.png")
