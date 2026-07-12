from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).parents[1] / "src/main/resources/assets/hearth_and_harvest/textures/block"

def texture(name, base):
    im = Image.new("RGBA", (16, 16), base)
    return im, ImageDraw.Draw(im), OUT / f"{name}.png"

im, d, path = texture("cutting_board_top", "#a87949")
d.rectangle((0,0,15,1), fill="#d09b5f"); d.rectangle((0,14,15,15), fill="#664128")
d.line((2,3,13,3), fill="#bc8952"); d.line((3,11,12,11), fill="#805332")
d.rectangle((12,1,14,3), fill="#5e3c25"); im.save(path)

im, d, path = texture("cutting_board_side", "#8e5c37")
d.rectangle((0,0,15,3), fill="#c08a52"); d.rectangle((0,12,15,15), fill="#5f3c28"); im.save(path)

im, d, path = texture("cooking_pot", "#555c62")
d.rectangle((0,0,15,2), fill="#9ca3a5"); d.rectangle((0,13,15,15), fill="#272b2e")
d.line((3,3,3,12), fill="#737b80"); d.line((12,3,12,12), fill="#353a3f"); im.save(path)

im, d, path = texture("cooking_pot_top", "#24282b")
d.rectangle((0,0,15,15), fill="#777f83"); d.rectangle((2,2,13,13), fill="#202427")
d.rectangle((4,4,11,11), fill="#5e3226"); d.point((6,6), fill="#b66a35"); d.point((10,8), fill="#78a044"); im.save(path)

im, d, path = texture("market_crate", "#875734")
d.rectangle((0,0,15,2), fill="#c08750"); d.rectangle((0,13,15,15), fill="#563622")
d.rectangle((1,3,3,12), fill="#a66e40"); d.rectangle((12,3,14,12), fill="#684128")
d.line((4,4,11,11), fill="#c08750"); d.line((11,4,4,11), fill="#5b3925"); im.save(path)
