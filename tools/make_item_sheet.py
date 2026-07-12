from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).parents[1]
textures = root / "src/main/resources/assets/hearth_and_harvest/textures"
names = [
    "tomato", "onion", "cucumber", "corn", "bell_pepper", "strawberry", "rice", "spinach",
    "tomato_seeds", "onion_seeds", "cucumber_seeds", "corn_seeds", "bell_pepper_seeds", "strawberry_seeds", "rice_seeds", "spinach_seeds",
    "flour", "cooking_oil", "dough", "cheese", "toast", "garden_salad", "tomato_soup", "veggie_stew",
    "stuffed_pepper", "strawberry_tart", "corn_chowder", "fried_rice", "farmers_breakfast", "cutting_board", "cooking_pot", "market_crate",
]
sheet = Image.new("RGBA", (512, 256), "#252a31")
draw = ImageDraw.Draw(sheet)
for y in range(0, 256, 16):
    for x in range(0, 512, 16):
        if (x // 16 + y // 16) % 2:
            draw.rectangle((x, y, x + 15, y + 15), fill="#303740")
for index, name in enumerate(names):
    path = textures / "item" / f"{name}.png"
    if not path.exists():
        path = textures / "block" / f"{name}.png"
    icon = Image.open(path).convert("RGBA").resize((64, 64), Image.Resampling.NEAREST)
    x = (index % 8) * 64
    y = (index // 8) * 64
    sheet.alpha_composite(icon, (x, y))
(root / "art").mkdir(exist_ok=True)
sheet.save(root / "art/item-sheet-preview.png")
