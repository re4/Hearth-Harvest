package com.mirinsworkshop.hearthandharvest;

import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.CropBlock;

import java.util.function.Supplier;

public final class HarvestCropBlock extends CropBlock {
    private final Supplier<Item> seeds;

    public HarvestCropBlock(Properties properties, Supplier<Item> seeds) {
        super(properties);
        this.seeds = seeds;
    }

    @Override
    protected Item getBaseSeedId() {
        return seeds.get();
    }
}
