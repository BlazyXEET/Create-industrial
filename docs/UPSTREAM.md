# Upstream source used

Repository: https://github.com/BlazyXEET/Create-industrial
Base commit: 9f04ad2110c4f2547b0a9fee676d794009345bc7

The builder explicitly checks out this revision rather than silently overlaying
unknown future changes. It applies the local source patch in a disposable checkout.
No upstream branches or commits were created.

These original textures were retrieved at that revision and their Git blob hashes
were checked before copying them into the complete overlay:

| File | Git blob SHA-1 |
| --- | --- |
| block_of_aluminium.png | 78f9aba804c8f6799f8d4dcd8cdde40a49f3104d |
| condensing_mesh.png | 155dff3d64336989ad98b508f438432e6fd64db8 |
| reinforced_concrete.png | 38b2851c87e3bc7dca5294aca8ce64feb7e27abb |
| reinforced_concrete_top.png | f5f76f1fd5e268650ec54cacaf6dc802a7b8eb7e |
| plastered_reinforced_concrete.png | a8a4996d6138a5714d4fdc13ded7a51238e06eff |

References for the interaction and registration changes:
- NeoForge 1.21.1 IItemExtension.onItemUseFirst, RegisterPayloadHandlersEvent,
  RegisterMenuScreensEvent, InputEvent.InteractionKeyMappingTriggered and GameTest documentation.
- Create mc1.21.1/dev IWrenchable API and its Catnip outline renderer.

Reading a moving development branch is not a substitute for compiling against
the pinned Maven dependencies. Those API checks remain part of the local build.
