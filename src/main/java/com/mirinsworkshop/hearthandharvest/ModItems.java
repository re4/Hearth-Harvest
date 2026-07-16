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

    public static final Item TOMATO = registerFood("tomato", 2, 0.25F);
    public static final Item ONION = registerFood("onion", 2, 0.2F);
    public static final Item CUCUMBER = registerFood("cucumber", 2, 0.25F);
    public static final Item CORN = registerFood("corn", 3, 0.3F);
    public static final Item BELL_PEPPER = registerFood("bell_pepper", 2, 0.25F);
    public static final Item STRAWBERRY = registerFood("strawberry", 2, 0.25F);
    public static final Item RICE = register("rice", Item::new, new Item.Properties());
    public static final Item SPINACH = registerFood("spinach", 2, 0.2F);

    public static final Item TOMATO_SEEDS = registerSeeds("tomato", ModBlocks.TOMATO_CROP);
    public static final Item ONION_SEEDS = registerSeeds("onion", ModBlocks.ONION_CROP);
    public static final Item CUCUMBER_SEEDS = registerSeeds("cucumber", ModBlocks.CUCUMBER_CROP);
    public static final Item CORN_SEEDS = registerSeeds("corn", ModBlocks.CORN_CROP);
    public static final Item BELL_PEPPER_SEEDS = registerSeeds("bell_pepper", ModBlocks.BELL_PEPPER_CROP);
    public static final Item STRAWBERRY_SEEDS = registerSeeds("strawberry", ModBlocks.STRAWBERRY_CROP);
    public static final Item RICE_SEEDS = registerSeeds("rice", ModBlocks.RICE_CROP);
    public static final Item SPINACH_SEEDS = registerSeeds("spinach", ModBlocks.SPINACH_CROP);

    public static final Item FLOUR = register("flour", Item::new, new Item.Properties());
    public static final Item COOKING_OIL = register("cooking_oil", Item::new, new Item.Properties().stacksTo(16));
    public static final Item DOUGH = register("dough", Item::new, new Item.Properties());
    public static final Item CHEESE = registerFood("cheese", 3, 0.5F);
    public static final Item TOAST = registerFood("toast", 5, 0.6F);
    public static final Item GRILLED_CHEESE = registerFood("grilled_cheese", 10, 1.0F);
    public static final Item GARDEN_SALAD = registerFood("garden_salad", 7, 0.8F);
    public static final Item TOMATO_SOUP = registerFood("tomato_soup", 8, 0.9F);
    public static final Item VEGGIE_STEW = registerFood("veggie_stew", 10, 1.0F);
    public static final Item STUFFED_PEPPER = registerFood("stuffed_pepper", 9, 0.9F);
    public static final Item STRAWBERRY_TART = registerFood("strawberry_tart", 8, 0.8F);
    public static final Item CORN_CHOWDER = registerFood("corn_chowder", 9, 0.9F);
    public static final Item FRIED_RICE = registerFood("fried_rice", 10, 1.0F);
    public static final Item FARMERS_BREAKFAST = registerFood("farmers_breakfast", 12, 1.2F);

    public static final Item CUTTING_BOARD = blockItem("cutting_board", ModBlocks.CUTTING_BOARD);
    public static final Item COOKING_POT = blockItem("cooking_pot", ModBlocks.COOKING_POT);
    public static final Item MARKET_CRATE = blockItem("market_crate", ModBlocks.MARKET_CRATE);

    static Item registerFood(String name, int nutrition, float saturation) {
        return register(name, Item::new, new Item.Properties().food(
                new FoodProperties.Builder().nutrition(nutrition).saturationModifier(saturation).build()));
    }

    static Item registerSeeds(String name, Block crop) {
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
