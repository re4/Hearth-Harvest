from pathlib import Path
from PIL import Image

root = Path(__file__).parents[1]
textures = root / "src/main/resources/assets/hearth_and_harvest/textures/block"
crops = ["tomato", "onion", "cucumber", "corn", "bell_pepper", "strawberry", "rice", "spinach"]
sheet = Image.new("RGBA", (512, 512), "#6f9e4c")
for row, crop in enumerate(crops):
    for age in range(8):
        icon = Image.open(textures / f"{crop}_stage{age}.png").resize((64, 64), Image.Resampling.NEAREST)
        sheet.alpha_composite(icon, (age * 64, row * 64))
sheet.save(root / "crop-sheet.png")
