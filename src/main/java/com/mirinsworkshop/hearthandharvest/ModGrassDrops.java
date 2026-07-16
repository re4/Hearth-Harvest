package com.mirinsworkshop.hearthandharvest;

import net.fabricmc.fabric.api.event.player.PlayerBlockBreakEvents;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

import java.util.ArrayList;
import java.util.List;

/** Adds a small server-side chance for broken grass to yield one random crop seed. */
public final class ModGrassDrops {
    private static final float SEED_CHANCE = 0.08F;

    public static void initialize() {
        List<Item> seeds = new ArrayList<>(List.of(
                ModItems.TOMATO_SEEDS,
                ModItems.ONION_SEEDS,
                ModItems.CUCUMBER_SEEDS,
                ModItems.CORN_SEEDS,
                ModItems.BELL_PEPPER_SEEDS,
                ModItems.STRAWBERRY_SEEDS,
                ModItems.RICE_SEEDS,
                ModItems.SPINACH_SEEDS
        ));
        seeds.addAll(ModExpandedCrops.seedItems());

        PlayerBlockBreakEvents.AFTER.register((level, player, pos, state, blockEntity) -> {
            if (level.isClientSide() || player.isCreative()) {
                return;
            }

            if (!state.is(Blocks.SHORT_GRASS) && !state.is(Blocks.TALL_GRASS)) {
                return;
            }

            if (level.getRandom().nextFloat() < SEED_CHANCE) {
                Item seed = seeds.get(level.getRandom().nextInt(seeds.size()));
                Block.popResource(level, pos, new ItemStack(seed));
            }
        });
    }

    private ModGrassDrops() {}
}
