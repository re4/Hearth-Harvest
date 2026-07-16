"""Validate packaged metadata, JSON, and every item sprite."""
from __future__ import annotations

import ast
import io
import json
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parents[1]
JAR = ROOT / "build/libs/hearth-and-harvest-1.1.0.jar"


def assigned_list(path: Path, variable: str) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == variable for target in node.targets)
    )


def component_sizes(texture: Image.Image) -> list[int]:
    occupied = {
        (x, y)
        for y in range(texture.height)
        for x in range(texture.width)
        if texture.getpixel((x, y))[3]
    }
    components = []
    while occupied:
        first = occupied.pop()
        component = {first}
        pending = [first]
        while pending:
            x, y = pending.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    neighbor = (x + dx, y + dy)
                    if neighbor in occupied:
                        occupied.remove(neighbor)
                        component.add(neighbor)
                        pending.append(neighbor)
        components.append(len(component))
    return sorted(components, reverse=True)


def expected_seed_label(crop_icon: Image.Image) -> Image.Image:
    icon = crop_icon.convert("RGBA")
    bounds = icon.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("Cannot validate a seed packet against an empty crop icon")
    icon = icon.crop(bounds)
    scale = min(6 / icon.width, 5 / icon.height)
    size = (max(1, round(icon.width * scale)), max(1, round(icon.height * scale)))
    icon = icon.resize(size, Image.Resampling.NEAREST)
    icon.putalpha(icon.getchannel("A").point(lambda alpha: 255 if alpha else 0))
    bounds = icon.getchannel("A").getbbox()
    if bounds is None:
        raise RuntimeError("Crop icon vanished while validating its seed packet")
    icon = icon.crop(bounds)
    label = Image.new("RGBA", (8, 6), (237, 199, 125, 255))
    label.alpha_composite(icon, ((8 - icon.width) // 2, (6 - icon.height) // 2))
    return label


expanded_names = assigned_list(ROOT / "tools/generate_expanded_content.py", "NAMES")
base_names = assigned_list(ROOT / "tools/import_item_sheet.py", "NAMES")
food_tool_names = [*base_names[16:], "grilled_cheese"]
padded_names = [*expanded_names, *[name for name in base_names if not name.endswith("_seeds")], "grilled_cheese"]
seed_crop_names = [*base_names[:8], *expanded_names]

for path in (ROOT / "src/main/resources").rglob("*.json"):
    json.loads(path.read_text(encoding="utf-8"))

with zipfile.ZipFile(JAR) as archive:
    archive_names = set(archive.namelist())
    metadata = json.loads(archive.read("fabric.mod.json"))
    item_textures = [
        path for path in archive.namelist()
        if path.startswith("assets/hearth_and_harvest/textures/item/") and path.endswith(".png")
    ]
    texture_problems = []
    edge_touching = []
    for texture_path in item_textures:
        texture = Image.open(io.BytesIO(archive.read(texture_path))).convert("RGBA")
        pixels = [texture.getpixel((x, y)) for y in range(texture.height) for x in range(texture.width)]
        if texture.size != (16, 16):
            texture_problems.append((texture_path, "size", texture.size))
        if any(alpha not in (0, 255) for _, _, _, alpha in pixels):
            texture_problems.append((texture_path, "partial alpha"))
        if any(
            alpha and red >= 220 and blue >= 220 and green <= 45 and abs(red - blue) <= 35
            for red, green, blue, alpha in pixels
        ):
            texture_problems.append((texture_path, "magenta key residue"))
        bounds = texture.getchannel("A").getbbox()
        if not bounds or bounds[0] == 0 or bounds[1] == 0 or bounds[2] == 16 or bounds[3] == 16:
            edge_touching.append((texture_path, bounds))

    oversized_sprites = []
    off_center_sprites = []
    fragmented_food_tools = []
    dark_chroma_edges = []
    seed_packet_problems = []
    for name in padded_names:
        data = archive.read(f"assets/hearth_and_harvest/textures/item/{name}.png")
        texture = Image.open(io.BytesIO(data)).convert("RGBA")
        bounds = texture.getchannel("A").getbbox()
        if bounds and (bounds[2] - bounds[0] > 12 or bounds[3] - bounds[1] > 12):
            oversized_sprites.append((name, bounds))
        if bounds and (abs(bounds[0] - (16 - bounds[2])) > 1 or abs(bounds[1] - (16 - bounds[3])) > 1):
            off_center_sprites.append((name, bounds))

    for name in food_tool_names:
        data = archive.read(f"assets/hearth_and_harvest/textures/item/{name}.png")
        texture = Image.open(io.BytesIO(data)).convert("RGBA")
        components = component_sizes(texture)
        if len(components) != 1:
            fragmented_food_tools.append((name, components))
        for y in range(16):
            for x in range(16):
                red, green, blue, alpha = texture.getpixel((x, y))
                if not alpha or max(red, green, blue) > 100 or blue < red * 0.9 or blue < green * 1.2:
                    continue
                neighbors = [
                    (x + dx, y + dy)
                    for dx in (-1, 0, 1)
                    for dy in (-1, 0, 1)
                    if dx or dy
                ]
                if any(
                    nx < 0 or ny < 0 or nx >= 16 or ny >= 16
                    or not texture.getpixel((nx, ny))[3]
                    for nx, ny in neighbors
                ):
                    dark_chroma_edges.append((name, (x, y), (red, green, blue)))

    for name in seed_crop_names:
        crop_data = archive.read(f"assets/hearth_and_harvest/textures/item/{name}.png")
        seed_data = archive.read(f"assets/hearth_and_harvest/textures/item/{name}_seeds.png")
        crop = Image.open(io.BytesIO(crop_data)).convert("RGBA")
        packet = Image.open(io.BytesIO(seed_data)).convert("RGBA")
        bounds = packet.getchannel("A").getbbox()
        if bounds != (3, 2, 13, 15):
            seed_packet_problems.append((name, "packet bounds", bounds))
        components = component_sizes(packet)
        if len(components) != 1:
            seed_packet_problems.append((name, "detached components", components))
        actual_label = packet.crop((4, 8, 12, 14))
        expected_label = expected_seed_label(crop)
        if actual_label.tobytes() != expected_label.tobytes():
            seed_packet_problems.append((name, "wrong or missing crop icon"))

assert metadata["version"] == "1.1.0", metadata["version"]
assert not edge_touching, edge_touching
assert not oversized_sprites, oversized_sprites
assert not off_center_sprites, off_center_sprites
assert not fragmented_food_tools, fragmented_food_tools
assert not dark_chroma_edges, dark_chroma_edges
assert not seed_packet_problems, seed_packet_problems
assert not texture_problems, texture_problems
assert "com/mirinsworkshop/hearthandharvest/HearthAndHarvest.class" in archive_names
assert "com/mirinsworkshop/hearthandharvest/ModItems.class" not in archive_names
assert "com/mirinsworkshop/hearthandharvest/a.class" in archive_names
assert (ROOT / "build/proguard/mapping.txt").is_file()
print(
    f"version={metadata['version']} item_textures={len(item_textures)} "
    f"padded_item_sprites_checked={len(padded_names)} all_item_textures=16x16-rgba "
    f"edge_touching=0 max_nonseed_extent=12 centered=verified "
    f"food_tools=connected seed_packet_icons={len(seed_crop_names)} chroma_residue=0 json=valid "
    f"proguard=verified jar_bytes={JAR.stat().st_size}"
)
