# Hearth & Harvest

**CurseForge:** [Hearth & Harvest](https://www.curseforge.com/minecraft/mc-mods/hearth-harvest/preview)

An original food-and-farming expansion for Minecraft 26.2 on Fabric. Grow a
large North American produce catalog, stock a pantry, and cook useful meals.

## Included content

- 67 growable fruit, vegetable, grain, herb, and leafy-green crops
- 59 additions in version 2.0, from orchard fruit and berries to root vegetables
  and salad greens
- Random crop seeds from short and tall grass in Survival
- 3 kitchen/decor blocks: cutting board, cooking pot, and market crate
- 4 pantry staples and 10 prepared meals, each with its own recipe and food value
- Mature-crop loot with extra seed yields
- A dedicated Hearth & Harvest creative tab
- 151 registered inventory entries and more than 500 crop growth-stage textures
- Original Minecraft-inspired pixel artwork throughout

## Requirements

- Minecraft Java Edition 26.2
- Fabric Loader 0.19.3 or newer
- Fabric API 0.152.2+26.2
- Java 25

## Build

Run `gradlew.bat build` on Windows. ProGuard automatically creates the protected
release jar in `build/libs`; this is the jar without `-dev` or `-sources` in its
name and is the one to upload to CurseForge. The `-dev` jar is unobfuscated and
is kept only for debugging. The obfuscation map is written to
`build/proguard/mapping.txt` for readable crash reports.

## Design

Hearth & Harvest takes broad inspiration from the genre of large farming and
cooking mods while using its own code, names, recipes, balance, and artwork.
