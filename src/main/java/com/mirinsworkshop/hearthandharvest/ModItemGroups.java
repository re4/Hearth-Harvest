package com.mirinsworkshop.hearthandharvest;

import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

public final class ModItemGroups {
    public static final CreativeModeTab MAIN = Registry.register(
            BuiltInRegistries.CREATIVE_MODE_TAB,
            Identifier.fromNamespaceAndPath(HearthAndHarvest.MOD_ID, "main"),
            FabricCreativeModeTab.builder()
                    .icon(() -> new ItemStack(ModItems.TOMATO))
                    .title(Component.translatable("itemGroup.hearth_and_harvest.main"))
                    .displayItems((parameters, output) -> ModItems.ALL.values().forEach(output::accept))
                    .build()
    );

    public static void initialize() {}

    private ModItemGroups() {}
}
