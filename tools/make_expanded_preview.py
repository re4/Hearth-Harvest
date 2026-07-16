from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).parents[1]
items = root / "src/main/resources/assets/hearth_and_harvest/textures/item"
blocks = root / "src/main/resources/assets/hearth_and_harvest/textures/block"
names = [
    "banana","orange","lemon","lime","grapefruit","peach","pear","cherry","plum","apricot","nectarine","blueberry","raspberry","blackberry","cranberry","grape",
    "cantaloupe","pineapple","mango","avocado","kiwi","pomegranate","papaya","coconut","fig","date","persimmon","guava","passion_fruit","lettuce","cabbage","broccoli",
    "cauliflower","asparagus","celery","eggplant","zucchini","butternut_squash","green_beans","peas","radish","turnip","parsnip","sweet_potato","yam","okra","artichoke","brussels_sprouts",
    "kale","swiss_chard","arugula","mustard_greens","collard_greens","leek","scallion","garlic","ginger","jalapeno","chili_pepper"]
original_names = ["tomato","corn","cucumber","onion","rice","bell_pepper","spinach","strawberry"]

sheet = Image.new("RGBA", (512,512), "#252a31"); d=ImageDraw.Draw(sheet)
for y in range(0,512,16):
    for x in range(0,512,16):
        if (x//16+y//16)%2: d.rectangle((x,y,x+15,y+15),fill="#303740")
for i,name in enumerate(names):
    icon=Image.open(items/f"{name}.png").resize((64,64),Image.Resampling.NEAREST)
    sheet.alpha_composite(icon,((i%8)*64,(i//8)*64))
sheet.save(root/"art/expanded-produce-preview.png")

# Produce/packet pairs make it easy to confirm that seed drops no longer look
# like broken-off pieces of the neighboring crop.
pairs = Image.new("RGBA", (1024, 512), "#252a31"); pair_draw = ImageDraw.Draw(pairs)
for y in range(0, 512, 16):
    for x in range(0, 1024, 16):
        if (x//16+y//16)%2: pair_draw.rectangle((x,y,x+15,y+15),fill="#303740")
for i,name in enumerate(names):
    x=(i%8)*128; y=(i//8)*64
    produce=Image.open(items/f"{name}.png").resize((64,64),Image.Resampling.NEAREST)
    seeds=Image.open(items/f"{name}_seeds.png").resize((64,64),Image.Resampling.NEAREST)
    pairs.alpha_composite(produce,(x,y)); pairs.alpha_composite(seeds,(x+64,y))
pairs.save(root/"art/expanded-items-preview.png")

# All 67 packets at 4x scale, so the miniature crop emblems are easy to audit.
all_seed_names = [*original_names, *names]
seed_rows = (len(all_seed_names) + 7) // 8
packets = Image.new("RGBA", (512, seed_rows * 64), "#252a31")
packet_draw = ImageDraw.Draw(packets)
for y in range(0, packets.height, 16):
    for x in range(0, packets.width, 16):
        if (x//16+y//16)%2:
            packet_draw.rectangle((x,y,x+15,y+15),fill="#303740")
for index, name in enumerate(all_seed_names):
    packet = Image.open(items/f"{name}_seeds.png").resize((64,64),Image.Resampling.NEAREST)
    packets.alpha_composite(packet,((index%8)*64,(index//8)*64))
packets.save(root/"art/seed-packets-preview.png")

samples=["banana","orange","blueberry","grape","lettuce","broccoli","eggplant","radish","sweet_potato","okra","kale","garlic"]
growth=Image.new("RGBA",(512,len(samples)*64),"#6f9e4c")
for row,name in enumerate(samples):
    for age in range(8):
        icon=Image.open(blocks/f"{name}_stage{age}.png").resize((64,64),Image.Resampling.NEAREST)
        growth.alpha_composite(icon,(age*64,row*64))
growth.save(root/"art/expanded-growth-preview.png")
