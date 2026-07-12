package com.mirinsworkshop.hearthandharvest;

import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class HearthAndHarvest implements ModInitializer {
    public static final String MOD_ID = "hearth_and_harvest";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        ModBlocks.initialize();
        ModItems.initialize();
        ModItemGroups.initialize();
        ModGrassDrops.initialize();
        LOGGER.info("Hearth & Harvest has set the table.");
    }
}
