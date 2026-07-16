package com.mirinsworkshop.hearthandharvest;

import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** The large 2.0 produce catalog, registered from compact data-driven specs. */
public final class ModExpandedCrops {
    public record CropEntry(String name, Item produce, Item seeds, Block crop) {}

    private static final String[] NAMES = {
            "banana", "orange", "lemon", "lime", "grapefruit", "peach", "pear", "cherry",
            "plum", "apricot", "nectarine", "blueberry", "raspberry", "blackberry", "cranberry",
            "grape", "cantaloupe", "pineapple", "mango", "avocado", "kiwi", "pomegranate",
            "papaya", "coconut", "fig", "date", "persimmon", "guava", "passion_fruit",
            "lettuce", "cabbage", "broccoli", "cauliflower", "asparagus", "celery", "eggplant",
            "zucchini", "butternut_squash", "green_beans", "peas", "radish", "turnip", "parsnip",
            "sweet_potato", "yam", "okra", "artichoke", "brussels_sprouts", "kale", "swiss_chard",
            "arugula", "mustard_greens", "collard_greens", "leek", "scallion", "garlic", "ginger",
            "jalapeno", "chili_pepper"
    };

    private static final List<CropEntry> ENTRIES = new ArrayList<>();

    public static void initialize() {
        if (!ENTRIES.isEmpty()) return;
        for (String name : NAMES) {
            Item[] seedHolder = new Item[1];
            Block crop = ModBlocks.registerCrop(name, () -> seedHolder[0]);
            Item produce = ModItems.registerFood(name, nutrition(name), saturation(name));
            Item seeds = ModItems.registerSeeds(name, crop);
            seedHolder[0] = seeds;
            ENTRIES.add(new CropEntry(name, produce, seeds, crop));
        }
        HearthAndHarvest.LOGGER.info("Registered {} additional crops.", ENTRIES.size());
    }

    public static List<CropEntry> entries() {
        return Collections.unmodifiableList(ENTRIES);
    }

    public static List<Item> seedItems() {
        return ENTRIES.stream().map(CropEntry::seeds).toList();
    }

    private static int nutrition(String name) {
        return switch (name) {
            case "coconut", "avocado", "sweet_potato", "yam" -> 4;
            case "banana", "mango", "pineapple", "cantaloupe", "papaya" -> 3;
            default -> 2;
        };
    }

    private static float saturation(String name) {
        return switch (name) {
            case "coconut", "avocado" -> 0.6F;
            case "sweet_potato", "yam", "banana" -> 0.4F;
            default -> 0.25F;
        };
    }

    private ModExpandedCrops() {}
}
