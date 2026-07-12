package com.mirinsworkshop.hearthandharvest;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Function;

public final class ModBlocks {
    public static final Map<String, Block> CROPS = new LinkedHashMap<>();

    public static final Block TOMATO_CROP = crop("tomato", () -> ModItems.TOMATO_SEEDS);
    public static final Block ONION_CROP = crop("onion", () -> ModItems.ONION_SEEDS);
    public static final Block CUCUMBER_CROP = crop("cucumber", () -> ModItems.CUCUMBER_SEEDS);
    public static final Block CORN_CROP = crop("corn", () -> ModItems.CORN_SEEDS);
    public static final Block BELL_PEPPER_CROP = crop("bell_pepper", () -> ModItems.BELL_PEPPER_SEEDS);
    public static final Block STRAWBERRY_CROP = crop("strawberry", () -> ModItems.STRAWBERRY_SEEDS);
    public static final Block RICE_CROP = crop("rice", () -> ModItems.RICE_SEEDS);
    public static final Block SPINACH_CROP = crop("spinach", () -> ModItems.SPINACH_SEEDS);

    public static final Block CUTTING_BOARD = register("cutting_board", props -> new Block(props),
            BlockBehaviour.Properties.of().strength(1.2F).sound(SoundType.WOOD));
    public static final Block COOKING_POT = register("cooking_pot", props -> new Block(props),
            BlockBehaviour.Properties.of().strength(1.8F).sound(SoundType.METAL));
    public static final Block MARKET_CRATE = register("market_crate", props -> new Block(props),
            BlockBehaviour.Properties.ofFullCopy(Blocks.BARREL));

    private static Block crop(String name, java.util.function.Supplier<net.minecraft.world.item.Item> seeds) {
        Block block = register(name + "_crop", props -> new HarvestCropBlock(props, seeds),
                BlockBehaviour.Properties.ofFullCopy(Blocks.WHEAT).noCollision().randomTicks().instabreak());
        CROPS.put(name, block);
        return block;
    }

    private static Block register(String name, Function<BlockBehaviour.Properties, Block> factory,
                                  BlockBehaviour.Properties properties) {
        Identifier id = Identifier.fromNamespaceAndPath(HearthAndHarvest.MOD_ID, name);
        ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, id);
        Block block = factory.apply(properties.setId(key));
        return net.minecraft.core.Registry.register(BuiltInRegistries.BLOCK, key, block);
    }

    public static void initialize() {}

    private ModBlocks() {}
}
