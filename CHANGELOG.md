# Changelog

## 1.1.1

- Reworked the cooking pot recipe so it no longer conflicts with the vanilla bucket recipe.
- Reworked the market crate recipe so it no longer conflicts with the vanilla chest recipe.
- Verified all 25 Hearth & Harvest recipes against Minecraft 26.2.
- Matched the cutting board selection and collision shape to its thin block model.
- Prevented the cutting board outline from appearing through neighboring walls.
- Disabled full-block occlusion for correct wall faces and lighting around the board.
- Matched the cooking pot outline and collision to its body and handles.

## 1.1.0

- Added the matching miniature crop icon to every one of the 67 seed packets.
- Enlarged the packet label so long and narrow crop silhouettes remain readable.
- Prevented the original item-sheet importer from replacing icon-labeled packets.
- Added exact validation that every packet contains the correct crop artwork.

## 2.0.7

- Audited all pantry items, prepared foods, kitchen tools, and placed kitchen textures.
- Restored the complete tops of nine food/tool sprites clipped by the old source-sheet grid.
- Resized every non-seed item silhouette into a centered area no larger than 12x12 pixels.
- Recolored dark magenta key fringes without deleting any silhouette pixels.
- Added validation for all 151 item textures and single-piece food/tool silhouettes.

## 2.0.6

- Replaced misaligned grid slicing with full-object extraction for all 59 expanded crops.
- Restored complete leaves, stems, roots, and bodies on 35 previously clipped produce sprites.
- Resized each complete silhouette into a padded 12x12 area on its 16x16 item canvas.
- Removed destructive color cleanup that mistook legitimate purple produce for background.

## 2.0.5

- Rebuilt every item texture on the official 16x16 Fabric item canvas.
- Removed remaining magenta-key fringes and purple generated drop shadows.
- Enforced hard RGBA transparency with no partially transparent edge pixels.
- Removed only one- and two-pixel islands while preserving complete produce.

## 2.0.4

- Fixed produce sprites that lost stems, roots, leaf tips, or outer pixels.
- Replaced aggressive fragment cleanup with full-silhouette preservation.
- Kept isolated generated shadow dots removed without trimming real artwork.

## 2.0.3

- Added ProGuard 7.9.1 to the release build for Java 25-compatible obfuscation.
- Preserved the Fabric entrypoint and mod resources with explicit keep rules.
- Release builds now produce a protected upload jar and a separate `-dev` jar.

## 2.0.2

- Added grilled cheese as a filling prepared meal.
- Added a shapeless recipe using two toast and one cheese.
- Added a matching Minecraft-inspired item sprite.

## 2.0.1

- Replaced fragment-like seed clusters with clear, connected seed packets.
- Reworked expanded produce sprites to use whole, intact fruit and vegetables.
- Added extra transparent padding so item artwork is not clipped at slot edges.

## 2.0.0

- Added 59 new growable produce crops, bringing the total to 67.
- Added bananas, citrus, stone fruit, berries, tropical fruit, melons, leafy
  greens, brassicas, legumes, roots, alliums, squash, peppers, and more.
- Added 118 matching produce and seed items.
- Added 472 new crop growth-stage textures and corresponding models.
- Added mature harvest loot and grass-seed discovery for every new crop.
- Expanded the creative tab, translations, and food-value balancing.

## 1.0.0

- First stable release of Hearth & Harvest.
- Includes eight crops, grass seed drops, pantry ingredients, prepared meals,
  kitchen blocks, dedicated-server support, and the redesigned pixel-art set.

## 0.3.1

- Changed grass seed drops to a direct server-side block-break event.
- Seed drops now work reliably with either shears or an empty hand in Survival.

## 0.3.0

- Short grass and tall grass now have an 8% chance to drop one random crop seed.
- The new drops are additive and do not replace vanilla wheat-seed drops.

## 0.2.1

- Removed detached shadow pixels that appeared as dots below some dropped items.
- Recentered affected sprites after cleanup.

## 0.2.0

- Rebuilt all 32 inventory sprites in a cohesive, vanilla-inspired pixel-art style.
- Added clearer silhouettes, material shading, and distinct meal presentation.
- Redesigned all 64 crop growth-stage textures.
- Added custom visual models for the cutting board and cooking pot.
- Improved market crate and kitchen-block textures.

## 0.1.1

- Added the Minecraft 26.2 client-item definitions required to display item models.

## 0.1.0

- Initial playable release.
