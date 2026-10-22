
package net.createindustrialteam.createindustrial.items;

import net.createindustrialteam.createindustrial.CreateIndustrial;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

public class ModCreativeModTabs {
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TAB =
            DeferredRegister.create(
                    Registries.CREATIVE_MODE_TAB,
                    CreateIndustrial.MODID
            );

    public static final Supplier<CreativeModeTab> CREATE_INDUSTRIAL_TAB =
            CREATIVE_MODE_TAB.register("create_industrial_tab",
                    () -> CreativeModeTab.builder()
                            .icon(() -> new ItemStack(ModItems.STEEL_INGOT.get()))
                            .title(Component.translatable(
                                    "creativetab.createindustrial.create_industrial"
                            ))
                            .displayItems((itemDisplayParameters, output) -> {
                                ModItems.ITEMS.getEntries().forEach(item ->
                                        output.accept(item.get())
                                );
                            })
                            .build()
            );

    public static void register(IEventBus event) {
        CREATIVE_MODE_TAB.register(event);
    }
}
