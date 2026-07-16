"""Generate the 2.0 crop resource pack from the approved produce sheet."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parents[1]
ASSETS = ROOT / "src/main/resources/assets/hearth_and_harvest"
DATA = ROOT / "src/main/resources/data/hearth_and_harvest"
SOURCE = ROOT / "art/source-expanded-produce-sheet-v3.png"

NAMES = [
    "banana", "orange", "lemon", "lime", "grapefruit", "peach", "pear", "cherry",
    "plum", "apricot", "nectarine", "blueberry", "raspberry", "blackberry", "cranberry", "grape",
    "cantaloupe", "pineapple", "mango", "avocado", "kiwi", "pomegranate", "papaya", "coconut",
    "fig", "date", "persimmon", "guava", "passion_fruit", "lettuce", "cabbage", "broccoli",
    "cauliflower", "asparagus", "celery", "eggplant", "zucchini", "butternut_squash", "green_beans", "peas",
    "radish", "turnip", "parsnip", "sweet_potato", "yam", "okra", "artichoke", "brussels_sprouts",
    "kale", "swiss_chard", "arugula", "mustard_greens", "collard_greens", "leek", "scallion", "garlic",
    "ginger", "jalapeno", "chili_pepper",
]

ORIGINAL_NAMES = [
    "tomato", "corn", "cucumber", "onion", "rice", "bell_pepper", "spinach", "strawberry",
]

DISPLAY_OVERRIDES = {
    "kiwi": "Kiwi", "passion_fruit": "Passion Fruit", "green_beans": "Green Beans",
    "sweet_potato": "Sweet Potato", "butternut_squash": "Butternut Squash",
    "brussels_sprouts": "Brussels Sprouts", "swiss_chard": "Swiss Chard",
    "mustard_greens": "Mustard Greens", "collard_greens": "Collard Greens",
    "jalapeno": "Jalapeño", "chili_pepper": "Chili Pepper",
}

ROOT_CROPS = {"radish", "turnip", "parsnip", "sweet_potato", "yam", "garlic", "ginger"}
LEAFY_CROPS = {
    "lettuce", "cabbage", "broccoli", "cauliflower", "celery", "artichoke",
    "brussels_sprouts", "kale", "swiss_chard", "arugula", "mustard_greens", "collard_greens",
}
VINE_CROPS = {
    "grape", "cantaloupe", "passion_fruit", "zucchini", "butternut_squash",
    "green_beans", "peas", "blueberry", "raspberry", "blackberry", "cranberry",
}
ORCHARD_CROPS = {
    "banana", "orange", "lemon", "lime", "grapefruit", "peach", "pear", "cherry", "plum",
    "apricot", "nectarine", "pineapple", "mango", "avocado", "kiwi", "pomegranate", "papaya",
    "coconut", "fig", "date", "persimmon", "guava",
}

MAX_SPRITE_EXTENT = 12


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def chroma_distance_squared(pixel) -> int:
    red, green, blue, _ = pixel
    return (255 - red) ** 2 + green ** 2 + (255 - blue) ** 2


def is_source_chroma(pixel) -> bool:
    """Match only the sheet's actual hot-magenta key, not purple produce."""
    red, green, blue, alpha = pixel
    return bool(alpha) and red >= 220 and blue >= 220 and green <= 45 and abs(red - blue) <= 35


def remove_connected_chroma(image: Image.Image) -> Image.Image:
    """Flood away the connected magenta backdrop from the full source sheet."""
    pixels = image.load()
    limit = 210 ** 2
    pending: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for x in range(image.width):
        pending.extend(((x, 0), (x, image.height - 1)))
    for y in range(image.height):
        pending.extend(((0, y), (image.width - 1, y)))

    while pending:
        x, y = pending.pop()
        point = (x, y)
        if point in seen or chroma_distance_squared(pixels[x, y]) > limit:
            continue
        seen.add(point)
        pixels[x, y] = (0, 0, 0, 0)
        if x > 0: pending.append((x - 1, y))
        if x + 1 < image.width: pending.append((x + 1, y))
        if y > 0: pending.append((x, y - 1))
        if y + 1 < image.height: pending.append((x, y + 1))
    return image


def extract_source_sprites(sheet: Image.Image) -> dict[str, Image.Image]:
    """Extract each complete produce object instead of slicing a misaligned grid."""
    keyed = remove_connected_chroma(sheet.convert("RGBA"))
    # Loops in multi-part drawings (notably the cherry stems) can enclose a
    # pocket of backdrop that a border flood cannot reach. Removing only the
    # exact source-key range clears those pockets without touching real purple.
    for y in range(keyed.height):
        for x in range(keyed.width):
            if is_source_chroma(keyed.getpixel((x, y))):
                keyed.putpixel((x, y), (0, 0, 0, 0))
    occupied = {
        (x, y)
        for y in range(keyed.height)
        for x in range(keyed.width)
        if keyed.getpixel((x, y))[3]
    }
    components: list[set[tuple[int, int]]] = []
    while occupied:
        first = occupied.pop()
        component = {first}
        pending = [first]
        while pending:
            x, y = pending.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (x + dx, y + dy)
                    if neighbor in occupied:
                        occupied.remove(neighbor)
                        component.add(neighbor)
                        pending.append(neighbor)
        components.append(component)

    # The approved sheet contains 59 large, connected produce drawings and a
    # few tiny generated specks. Taking the 59 largest components preserves
    # every leaf/root while discarding only those unrelated specks.
    components.sort(key=len, reverse=True)
    components = components[:len(NAMES)]
    if len(components) != len(NAMES):
        raise RuntimeError(f"Expected {len(NAMES)} produce objects, found {len(components)}")

    sprites: dict[str, Image.Image] = {}
    for component in components:
        center_x = sum(x for x, _ in component) / len(component)
        center_y = sum(y for _, y in component) / len(component)
        col = round(center_x * 8 / keyed.width - 0.5)
        row = round(center_y * 8 / keyed.height - 0.5)
        index = row * 8 + col
        if not (0 <= col < 8 and 0 <= row < 8 and index < len(NAMES)):
            raise RuntimeError(f"Produce object at {(center_x, center_y)} is outside the expected layout")
        name = NAMES[index]
        if name in sprites:
            raise RuntimeError(f"More than one source object mapped to {name}")

        left = min(x for x, _ in component)
        top = min(y for _, y in component)
        right = max(x for x, _ in component) + 1
        bottom = max(y for _, y in component) + 1
        sprite = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
        for x, y in component:
            sprite.putpixel((x - left, y - top), keyed.getpixel((x, y)))
        sprites[name] = sprite

    missing = set(NAMES) - sprites.keys()
    if missing:
        raise RuntimeError(f"Missing source objects: {sorted(missing)}")
    return sprites


def to_sprite(source: Image.Image, name: str) -> Image.Image:
    box = source.getchannel("A").getbbox()
    if box is None:
        raise RuntimeError(f"Empty source sprite for {name}")
    crop = source.crop(box)
    # The full source silhouette is resized as one object. A 12x12 maximum
    # leaves two transparent pixels around even the bulkiest item on its 16x16
    # Minecraft canvas, so nothing can be clipped in inventory or on the ground.
    scale = min(MAX_SPRITE_EXTENT / crop.width, MAX_SPRITE_EXTENT / crop.height)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    crop = crop.resize(size, Image.Resampling.NEAREST)
    alpha = crop.getchannel("A").point(lambda a: 255 if a else 0)
    crop = crop.convert("RGB").quantize(colors=15, method=Image.Quantize.MEDIANCUT).convert("RGBA")
    crop.putalpha(alpha)
    out = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    out.alpha_composite(crop, ((16-crop.width)//2, (16-crop.height)//2))
    return out


def palette(sprite: Image.Image) -> tuple[str, str, str]:
    colors = Counter(p[:3] for p in sprite.getdata() if p[3] and not (p[1] > p[0] * 1.35 and p[1] > p[2] * 1.25))
    if not colors: colors = Counter(p[:3] for p in sprite.getdata() if p[3])
    common = [c for c, _ in colors.most_common(8)]
    base = common[0]
    dark = tuple(max(0, int(v * .62)) for v in base)
    light = tuple(min(255, int(v * 1.22 + 14)) for v in base)
    return tuple("#%02x%02x%02x" % c for c in (dark, base, light))


def make_seeds(crop_icon: Image.Image) -> Image.Image:
    """Draw a seed packet with a miniature matching crop icon on its label."""
    out = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    # A connected paper packet reads as "seeds" instead of looking like a
    # handful of detached/cut-off pixels when dropped on the ground.
    outline, paper_dark, paper, paper_light = "#3b2818", "#8b5a2b", "#c98a45", "#edc77d"
    d.rectangle((3, 2, 12, 14), fill=outline)
    d.rectangle((4, 3, 11, 13), fill=paper)
    d.line((4, 3, 7, 6, 11, 3), fill=paper_light)
    d.line((4, 4, 7, 7, 11, 4), fill=paper_dark)
    d.rectangle((4, 8, 11, 13), fill=paper_light)

    icon = crop_icon.convert("RGBA")
    bounds = icon.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("Cannot put an empty crop icon on a seed packet")
    icon = icon.crop(bounds)
    scale = min(6 / icon.width, 5 / icon.height)
    size = (max(1, round(icon.width * scale)), max(1, round(icon.height * scale)))
    icon = icon.resize(size, Image.Resampling.NEAREST)
    icon.putalpha(icon.getchannel("A").point(lambda alpha: 255 if alpha else 0))
    resized_bounds = icon.getchannel("A").getbbox()
    if resized_bounds is None:
        raise RuntimeError("Crop icon vanished while making its seed packet")
    icon = icon.crop(resized_bounds)
    out.alpha_composite(icon, (4 + (8 - icon.width) // 2, 8 + (6 - icon.height) // 2))
    return out


def make_crop_stage(name: str, age: int, fruit: tuple[str, str, str]) -> Image.Image:
    dark_fruit, base_fruit, light_fruit = fruit
    im = Image.new("RGBA", (16,16), (0,0,0,0)); d = ImageDraw.Draw(im)
    green_dark, green, green_light = "#31572f", "#4f7d3b", "#75a84c"
    height = [2,3,5,7,9,11,13,14][age]; top = 15-height

    if name in ROOT_CROPS:
        width = min(4, 1 + age//2)
        for x in range(8-width, 9+width, 2):
            d.line((8,15,x,max(top,8)+abs(x-8)//2), fill=green)
            d.point((x,max(top,8)+abs(x-8)//2), fill=green_light)
        if age >= 6: d.rectangle((6,13,10,15), fill=base_fruit)
    elif name in LEAFY_CROPS:
        radius = min(6, 1+age)
        for x in range(8-radius,9+radius,2):
            y = 15 - (radius-abs(x-8))//2
            d.line((8,15,x,max(top,y-radius//2)), fill=green_dark)
            d.rectangle((x-1,max(top,y-radius//2),x+1,min(15,y+1)), fill=green if x%4 else green_light)
        if name in {"broccoli","cauliflower","artichoke","brussels_sprouts"} and age >= 6:
            d.ellipse((5,7,11,12), fill=light_fruit if name=="cauliflower" else base_fruit)
    elif name in VINE_CROPS:
        spread = min(6, 1+age)
        d.line((2,14,14,14), fill=green_dark)
        for x in range(3,14,3):
            d.line((x,14,x + (-1 if x%2 else 1), max(top,9)), fill=green)
            d.rectangle((x-1,max(top,9),x+1,max(top,10)), fill=green_light)
        if age >= 5:
            for x,y in ((5,12),(10,11),(8,8))[:age-4]: d.rectangle((x,y,x+1,y+1), fill=base_fruit)
    else:
        trunk = "#705235" if name in ORCHARD_CROPS and age >= 3 else green_dark
        d.line((8,15,8,top), fill=trunk)
        branches = min(4, age//2)
        for n in range(branches):
            y = 13-n*3; direction = -1 if n%2==0 else 1
            d.line((8,y,8+direction*4,y-2), fill=green_dark)
            x1, x2 = sorted((8+direction*2, 8+direction*4))
            d.rectangle((x1,y-3,x2,y-1), fill=green)
            d.point((8+direction*3,y-3), fill=green_light)
        if age >= 5:
            for x,y in ((5,11),(10,9),(6,7))[:age-4]:
                d.rectangle((x,y,x+1,y+1), fill=dark_fruit); d.point((x+1,y), fill=light_fruit)
    return im


sheet = Image.open(SOURCE).convert("RGBA")
source_sprites = extract_source_sprites(sheet)
lang_path = ASSETS / "lang/en_us.json"
lang = json.loads(lang_path.read_text(encoding="utf-8"))

for index, name in enumerate(NAMES):
    sprite = to_sprite(source_sprites[name], name)
    colors = palette(sprite)
    sprite.save(ASSETS / f"textures/item/{name}.png")
    make_seeds(sprite).save(ASSETS / f"textures/item/{name}_seeds.png")

    write_json(ASSETS / f"models/item/{name}.json", {
        "parent":"minecraft:item/generated", "textures":{"layer0":f"hearth_and_harvest:item/{name}"}})
    write_json(ASSETS / f"models/item/{name}_seeds.json", {
        "parent":"minecraft:item/generated", "textures":{"layer0":f"hearth_and_harvest:item/{name}_seeds"}})
    for item_name in (name, f"{name}_seeds"):
        write_json(ASSETS / f"items/{item_name}.json", {
            "model":{"type":"minecraft:model","model":f"hearth_and_harvest:item/{item_name}"}})

    variants = {f"age={age}":{"model":f"hearth_and_harvest:block/{name}_stage{age}"} for age in range(8)}
    write_json(ASSETS / f"blockstates/{name}_crop.json", {"variants":variants})
    for age in range(8):
        write_json(ASSETS / f"models/block/{name}_stage{age}.json", {
            "parent":"minecraft:block/crop", "textures":{"crop":f"hearth_and_harvest:block/{name}_stage{age}"}})
        make_crop_stage(name, age, colors).save(ASSETS / f"textures/block/{name}_stage{age}.png")

    mature = {"condition":"minecraft:block_state_property","block":f"hearth_and_harvest:{name}_crop","properties":{"age":"7"}}
    write_json(DATA / f"loot_table/blocks/{name}_crop.json", {
        "type":"minecraft:block",
        "pools":[
            {"rolls":1,"entries":[{"type":"minecraft:alternatives","children":[
                {"type":"minecraft:item","name":f"hearth_and_harvest:{name}","conditions":[mature]},
                {"type":"minecraft:item","name":f"hearth_and_harvest:{name}_seeds"}]}]},
            {"rolls":1,"conditions":[mature],"entries":[{"type":"minecraft:item","name":f"hearth_and_harvest:{name}_seeds",
                "functions":[{"function":"minecraft:set_count","count":{"type":"minecraft:uniform","min":0,"max":2}},
                             {"function":"minecraft:explosion_decay"}]}]},
        ], "random_sequence":f"hearth_and_harvest:blocks/{name}_crop"})

    display = DISPLAY_OVERRIDES.get(name, name.replace("_", " ").title())
    lang[f"item.hearth_and_harvest.{name}"] = display
    lang[f"item.hearth_and_harvest.{name}_seeds"] = f"{display} Seeds"

# Match the original eight seed items to the same icon-labeled packet design.
for name in ORIGINAL_NAMES:
    produce_path = ASSETS / f"textures/item/{name}.png"
    make_seeds(Image.open(produce_path).convert("RGBA")).save(
        ASSETS / f"textures/item/{name}_seeds.png"
    )

write_json(lang_path, lang)
print(f"Generated resources for {len(NAMES)} crops ({len(NAMES)*2} items, {len(NAMES)*8} growth textures).")
