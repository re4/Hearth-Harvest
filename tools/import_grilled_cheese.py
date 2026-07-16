"""Convert the approved grilled-cheese concept into a crisp 16px item sprite."""
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "art/source-grilled-cheese-v3.png"
OUTPUT = ROOT / "src/main/resources/assets/hearth_and_harvest/textures/item/grilled_cheese.png"
PREVIEW = ROOT / "art/grilled-cheese-preview.png"

source = Image.open(SOURCE).convert("RGBA")
pixels = source.load()
for y in range(source.height):
    for x in range(source.width):
        red, green, blue, _ = pixels[x, y]
        if red > 160 and blue > 130 and red > green * 1.5 and blue > green * 1.3:
            pixels[x, y] = (0, 0, 0, 0)
bounds = source.getchannel("A").getbbox()
if bounds is None:
    raise RuntimeError("The grilled-cheese source has no visible pixels")

sprite = source.crop(bounds)
scale = min(12 / sprite.width, 12 / sprite.height)
size = (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale)))
sprite = sprite.resize(size, Image.Resampling.LANCZOS)

alpha = sprite.getchannel("A").point(lambda value: 255 if value >= 96 else 0)
sprite = sprite.convert("RGB").quantize(colors=14, method=Image.Quantize.MEDIANCUT).convert("RGBA")
sprite.putalpha(alpha)

item = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
item.alpha_composite(sprite, ((16 - sprite.width) // 2, (16 - sprite.height) // 2))
item.save(OUTPUT)

preview = Image.new("RGBA", (256, 256), "#252a31")
draw = ImageDraw.Draw(preview)
for y in range(0, 256, 16):
    for x in range(0, 256, 16):
        if (x // 16 + y // 16) % 2:
            draw.rectangle((x, y, x + 15, y + 15), fill="#303740")
preview.alpha_composite(item.resize((256, 256), Image.Resampling.NEAREST))
preview.save(PREVIEW)
