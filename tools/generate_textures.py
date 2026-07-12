"""Generate the original 16px pixel-art asset set for Hearth & Harvest."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parents[1] / "src/main/resources/assets/hearth_and_harvest/textures"
ITEMS = ROOT / "item"
BLOCKS = ROOT / "block"
ITEMS.mkdir(parents=True, exist_ok=True)
BLOCKS.mkdir(parents=True, exist_ok=True)

PALETTES = {
    "tomato": ("#a51f24", "#ed4b3e", "#5c962f"),
    "onion": ("#b97a9b", "#efc6d8", "#6c9b42"),
    "cucumber": ("#267340", "#61b95a", "#b8d75c"),
    "corn": ("#d58b24", "#f4cf3c", "#5b963c"),
    "bell_pepper": ("#c72f2b", "#ef6b34", "#4d8a39"),
    "strawberry": ("#b91f3d", "#ef4361", "#4c963e"),
    "rice": ("#c7b87a", "#f0e1a2", "#6b9b43"),
    "spinach": ("#21643c", "#459956", "#8cc35a"),
}

def canvas():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))

def save_item(name, base, light, accent):
    im = canvas(); d = ImageDraw.Draw(im)
    if name in {"flour", "dough", "cheese", "toast"}:
        d.rectangle((3, 5, 12, 12), fill=base); d.rectangle((4, 4, 11, 10), fill=light)
        d.rectangle((5, 5, 6, 6), fill=accent); d.rectangle((10, 8, 11, 9), fill=accent)
    elif name == "cooking_oil":
        d.rectangle((6, 2, 9, 4), fill="#d9e6e1"); d.rectangle((4, 5, 11, 13), fill="#b8d1ca")
        d.rectangle((5, 8, 10, 12), fill="#e2bd32"); d.rectangle((6, 6, 9, 7), fill="#f7dc55")
    elif name in {"garden_salad", "tomato_soup", "veggie_stew", "corn_chowder", "fried_rice", "farmers_breakfast"}:
        d.rectangle((2, 7, 13, 11), fill="#6f4938"); d.rectangle((4, 12, 11, 13), fill="#4e322b")
        d.rectangle((3, 6, 12, 9), fill=base); d.rectangle((5, 6, 6, 7), fill=light); d.rectangle((9, 7, 10, 8), fill=accent)
    elif name in {"stuffed_pepper", "strawberry_tart"}:
        d.rectangle((3, 6, 12, 12), fill=base); d.rectangle((4, 5, 11, 9), fill=light); d.rectangle((6, 4, 7, 5), fill=accent)
    else:
        d.rectangle((4, 4, 11, 12), fill=base); d.rectangle((5, 3, 10, 10), fill=light)
        d.rectangle((7, 1, 8, 4), fill=accent); d.rectangle((9, 2, 11, 3), fill=accent)
        d.point((6, 6), fill="#fff2ba"); d.point((10, 8), fill=base)
    im.save(ITEMS / f"{name}.png")

for name, colors in PALETTES.items():
    save_item(name, *colors)
    im = canvas(); d = ImageDraw.Draw(im)
    d.rectangle((5, 7, 10, 9), fill=colors[1]); d.rectangle((7, 4, 8, 8), fill=colors[2]); d.point((6, 5), fill=colors[2]); d.point((9, 6), fill=colors[2])
    im.save(ITEMS / f"{name}_seeds.png")

extras = {
    "flour": ("#b79d72", "#f1dfb2", "#76583d"), "dough": ("#c49a64", "#ecc58d", "#9b6e42"),
    "cheese": ("#d89e22", "#ffd95a", "#a5691d"), "toast": ("#8f532d", "#d68a48", "#5d3725"),
    "garden_salad": ("#397b45", "#80bd58", "#d94236"), "tomato_soup": ("#9f2828", "#e34a3f", "#f4c34b"),
    "veggie_stew": ("#824b2e", "#b97136", "#75aa45"), "stuffed_pepper": ("#a92d29", "#e35b35", "#f2ca48"),
    "strawberry_tart": ("#8b4f2c", "#d93456", "#f09b62"), "corn_chowder": ("#c88b2f", "#f1d46b", "#7fa44b"),
    "fried_rice": ("#9c713d", "#e1c372", "#55934a"), "farmers_breakfast": ("#8a482d", "#e0a33a", "#f4df83"),
}
save_item("cooking_oil", "#e2bd32", "#f7dc55", "#b8d1ca")
for name, colors in extras.items(): save_item(name, *colors)

for crop, (dark, light, green) in PALETTES.items():
    for age in range(8):
        im = canvas(); d = ImageDraw.Draw(im); height = 2 + age * 2
        y0 = max(2, 15 - height)
        d.rectangle((7, y0, 8, 15), fill=green)
        for y in range(14, y0, -3):
            spread = min(5, 1 + age // 2)
            d.line((7, y, 7-spread, y-2), fill=green); d.line((8, y-1, 8+spread, y-3), fill=green)
        if age >= 5:
            d.rectangle((4, 8, 6, 10), fill=dark); d.rectangle((10, 6, 12, 8), fill=light)
        if age == 7: d.rectangle((7, 4, 9, 6), fill=light)
        im.save(BLOCKS / f"{crop}_stage{age}.png")

block_patterns = {
    "cutting_board": ("#765037", "#b57a4b", "#d19b62"),
    "cooking_pot": ("#31363b", "#626a70", "#9da5a7"),
    "market_crate": ("#5a3b29", "#96623b", "#c08750"),
}
for name, (dark, base, light) in block_patterns.items():
    im = Image.new("RGBA", (16,16), base); d = ImageDraw.Draw(im)
    d.rectangle((0,0,15,2), fill=light); d.rectangle((0,13,15,15), fill=dark)
    d.line((3,0,3,15), fill=dark); d.line((12,0,12,15), fill=dark)
    d.line((4,4,11,11), fill=light); d.line((11,4,4,11), fill=dark)
    im.save(BLOCKS / f"{name}.png")

icon = Image.open(ITEMS / "tomato.png").resize((128,128), Image.Resampling.NEAREST)
icon.save(ROOT.parent / "icon.png")
