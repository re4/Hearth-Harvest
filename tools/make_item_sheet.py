from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).parents[1]
textures = root / "src/main/resources/assets/hearth_and_harvest/textures"
names = [
    "tomato", "onion", "cucumber", "corn", "bell_pepper", "strawberry", "rice", "spinach",
    "tomato_seeds", "onion_seeds", "cucumber_seeds", "corn_seeds", "bell_pepper_seeds", "strawberry_seeds", "rice_seeds", "spinach_seeds",
    "flour", "cooking_oil", "dough", "cheese", "toast", "grilled_cheese", "garden_salad", "tomato_soup",
    "veggie_stew", "stuffed_pepper", "strawberry_tart", "corn_chowder", "fried_rice", "farmers_breakfast", "cutting_board", "cooking_pot", "market_crate",
]
sheet = Image.new("RGBA", (512, 320), "#252a31")
draw = ImageDraw.Draw(sheet)
for y in range(0, 320, 16):
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

food_tools = [
    "flour", "cooking_oil", "dough", "cheese", "toast", "grilled_cheese",
    "garden_salad", "tomato_soup", "veggie_stew", "stuffed_pepper",
    "strawberry_tart", "corn_chowder", "fried_rice", "farmers_breakfast",
    "cutting_board", "cooking_pot", "market_crate",
]
audit = Image.new("RGBA", (480, 384), "#252a31")
audit_draw = ImageDraw.Draw(audit)
for y in range(0, audit.height, 16):
    for x in range(0, audit.width, 16):
        if (x // 16 + y // 16) % 2:
            audit_draw.rectangle((x, y, x + 15, y + 15), fill="#303740")
for index, name in enumerate(food_tools):
    icon = Image.open(textures / "item" / f"{name}.png").convert("RGBA")
    icon = icon.resize((80, 80), Image.Resampling.NEAREST)
    x = (index % 5) * 96 + 8
    y = (index // 5) * 96 + 8
    audit.alpha_composite(icon, (x, y))
audit.save(root / "art/food-tools-preview.png")
