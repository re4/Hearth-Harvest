package com.mirinsworkshop.hearthandharvest;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.Identifier;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Function;

public final class ModItems {
    public static final Map<String, Item> ALL = new LinkedHashMap<>();

    public static final Item TOMATO = food("tomato", 2, 0.25F);
    public static final Item ONION = food("onion", 2, 0.2F);
    public static final Item CUCUMBER = food("cucumber", 2, 0.25F);
    public static final Item CORN = food("corn", 3, 0.3F);
    public static final Item BELL_PEPPER = food("bell_pepper", 2, 0.25F);
    public static final Item STRAWBERRY = food("strawberry", 2, 0.25F);
    public static final Item RICE = register("rice", Item::new, new Item.Properties());
    public static final Item SPINACH = food("spinach", 2, 0.2F);

    public static final Item TOMATO_SEEDS = seeds("tomato", ModBlocks.TOMATO_CROP);
    public static final Item ONION_SEEDS = seeds("onion", ModBlocks.ONION_CROP);
    public static final Item CUCUMBER_SEEDS = seeds("cucumber", ModBlocks.CUCUMBER_CROP);
    public static final Item CORN_SEEDS = seeds("corn", ModBlocks.CORN_CROP);
    public static final Item BELL_PEPPER_SEEDS = seeds("bell_pepper", ModBlocks.BELL_PEPPER_CROP);
    public static final Item STRAWBERRY_SEEDS = seeds("strawberry", ModBlocks.STRAWBERRY_CROP);
    public static final Item RICE_SEEDS = seeds("rice", ModBlocks.RICE_CROP);
    public static final Item SPINACH_SEEDS = seeds("spinach", ModBlocks.SPINACH_CROP);

    public static final Item FLOUR = register("flour", Item::new, new Item.Properties());
    public static final Item COOKING_OIL = register("cooking_oil", Item::new, new Item.Properties().stacksTo(16));
    public static final Item DOUGH = register("dough", Item::new, new Item.Properties());
    public static final Item CHEESE = food("cheese", 3, 0.5F);
    public static final Item TOAST = food("toast", 5, 0.6F);
    public static final Item GARDEN_SALAD = food("garden_salad", 7, 0.8F);
    public static final Item TOMATO_SOUP = food("tomato_soup", 8, 0.9F);
    public static final Item VEGGIE_STEW = food("veggie_stew", 10, 1.0F);
    public static final Item STUFFED_PEPPER = food("stuffed_pepper", 9, 0.9F);
    public static final Item STRAWBERRY_TART = food("strawberry_tart", 8, 0.8F);
    public static final Item CORN_CHOWDER = food("corn_chowder", 9, 0.9F);
    public static final Item FRIED_RICE = food("fried_rice", 10, 1.0F);
    public static final Item FARMERS_BREAKFAST = food("farmers_breakfast", 12, 1.2F);

    public static final Item CUTTING_BOARD = blockItem("cutting_board", ModBlocks.CUTTING_BOARD);
    public static final Item COOKING_POT = blockItem("cooking_pot", ModBlocks.COOKING_POT);
    public static final Item MARKET_CRATE = blockItem("market_crate", ModBlocks.MARKET_CRATE);

    private static Item food(String name, int nutrition, float saturation) {
        return register(name, Item::new, new Item.Properties().food(
                new FoodProperties.Builder().nutrition(nutrition).saturationModifier(saturation).build()));
    }

    private static Item seeds(String name, Block crop) {
        return register(name + "_seeds", props -> new BlockItem(crop, props), new Item.Properties());
    }

    private static Item blockItem(String name, Block block) {
        return register(name, props -> new BlockItem(block, props), new Item.Properties().useBlockDescriptionPrefix());
    }

    private static Item register(String name, Function<Item.Properties, Item> factory, Item.Properties properties) {
        Identifier id = Identifier.fromNamespaceAndPath(HearthAndHarvest.MOD_ID, name);
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
        Item item = factory.apply(properties.setId(key));
        ALL.put(name, item);
        return Registry.register(BuiltInRegistries.ITEM, key, item);
    }

    public static void initialize() {}

    private ModItems() {}
}
