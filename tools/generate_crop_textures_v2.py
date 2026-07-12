"""Generate distinctive, vanilla-scaled crop stages with hard pixel edges."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).parents[1] / "src/main/resources/assets/hearth_and_harvest/textures/block"
GREEN = {
    "tomato": ("#31592d", "#4f7d38", "#72a447"),
    "onion": ("#48743d", "#6c9a4c", "#91b95d"),
    "cucumber": ("#285b32", "#3f813d", "#65a64b"),
    "corn": ("#46672b", "#718d32", "#9caf3c"),
    "bell_pepper": ("#315b2e", "#4d7c36", "#70a248"),
    "strawberry": ("#315c32", "#4e853d", "#75a94d"),
    "rice": ("#6c7334", "#929548", "#b9ad5e"),
    "spinach": ("#285a35", "#397642", "#57984c"),
}
FRUIT = {
    "tomato": ("#8f2524", "#d24432"), "onion": ("#b37c9d", "#e1b6ce"),
    "cucumber": ("#28653a", "#4b9148"), "corn": ("#d29127", "#efc83a"),
    "bell_pepper": ("#9f2926", "#d7432f"), "strawberry": ("#a52238", "#df3850"),
    "rice": ("#c6ae69", "#e2d08c"), "spinach": ("#397642", "#6aa654"),
}
HEIGHTS = [3, 4, 6, 8, 10, 12, 14, 15]


def px(d, x, y, color):
    if 0 <= x < 16 and 0 <= y < 16:
        d.point((x, y), fill=color)


def leaf(d, x, y, direction, dark, mid, light, size=2):
    for n in range(size):
        px(d, x + direction * n, y - n // 2, mid)
    px(d, x + direction * size, y - max(0, size // 2), dark)
    if size > 1:
        px(d, x + direction, y - 1, light)


for crop in GREEN:
    dark, mid, light = GREEN[crop]
    fruit_dark, fruit_light = FRUIT[crop]
    for age, height in enumerate(HEIGHTS):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        top = 15 - height

        if crop == "spinach":
            width = 1 + age // 2
            for x in range(8 - width, 9 + width):
                rise = abs(x - 8) // 2
                d.line((8, 15, x, max(top + rise, 8)), fill=dark if x < 8 else mid)
                if age >= 3:
                    px(d, x, max(top + rise, 8), light)
            if age >= 5:
                d.rectangle((4, 11, 11, 14), fill=mid)
                d.rectangle((6, 9, 9, 14), fill=light)
        elif crop == "strawberry":
            d.line((8, 15, 8, max(top, 8)), fill=dark)
            spread = min(5, 1 + age)
            for x in range(8 - spread, 9 + spread, 2):
                y = 14 - (spread - abs(x - 8)) // 2
                d.line((8, 14, x, y), fill=dark)
                px(d, x, y, light if x % 4 else mid)
                px(d, x + (1 if x < 8 else -1), y + 1, mid)
            if age >= 5:
                for x, y in ((5, 12), (10, 11), (7, 9))[:age-4]:
                    px(d, x, y, fruit_dark); px(d, x, y+1, fruit_light)
        elif crop == "onion":
            bulb_w = 1 if age < 4 else 2 if age < 6 else 3
            d.rectangle((8 - bulb_w, 14 - bulb_w // 2, 8 + bulb_w, 15), fill=fruit_dark)
            if age >= 6: d.rectangle((7, 13, 9, 14), fill=fruit_light)
            stalks = min(5, 1 + age // 2)
            for n in range(stalks):
                x = 8 + n - stalks // 2
                d.line((x, 14, x + (-1 if n % 2 else 1), top + n % 3), fill=mid if n % 2 else light)
        elif crop == "rice":
            stalks = min(5, 1 + age // 2)
            for n in range(stalks):
                x = 8 + (n - stalks // 2) * 2
                d.line((x, 15, x + (-1 if n % 2 else 1), top + n % 2), fill=mid)
                if age >= 5:
                    for k in range(3): px(d, x + (-1 if n % 2 else 1), top + n % 2 + k*2, fruit_light if k == 0 else fruit_dark)
        else:
            # Upright branching plants: corn stays narrow; vines and nightshades spread.
            d.line((8, 15, 8, top), fill=dark)
            px(d, 9, top + 2, light)
            branch_count = min(4, age // 2)
            for n in range(branch_count):
                y = 13 - n * 3
                size = 3 if crop in {"cucumber", "tomato"} and age >= 5 else 2
                leaf(d, 8, y, -1 if n % 2 == 0 else 1, dark, mid, light, size)
                leaf(d, 8, y - 1, 1 if n % 2 == 0 else -1, dark, mid, light, max(1, size-1))
            if crop == "corn":
                for y in range(14, max(top + 2, 5), -3):
                    leaf(d, 8, y, -1 if y % 2 else 1, dark, mid, light, 3)
                if age >= 5:
                    d.rectangle((9, 8, 10, 11), fill=fruit_dark); px(d, 10, 8, fruit_light)
            elif age >= 5:
                positions = ((5, 11), (10, 9), (6, 7))
                for x, y in positions[:age-4]:
                    if crop == "cucumber":
                        d.line((x, y, x, y+2), fill=fruit_dark); px(d, x+1, y+1, fruit_light)
                    else:
                        d.rectangle((x, y, x+1, y+1), fill=fruit_dark); px(d, x+1, y, fruit_light)

        im.save(OUT / f"{crop}_stage{age}.png")

