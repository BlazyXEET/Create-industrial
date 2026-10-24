# Foundry processing — Small and Large

Both furnaces use the same server-owned hatch inventory and molten-metal tank. Accepted fuel: coal, charcoal, coal blocks and blaze rods. Raw iron, copper, and gold convert to 144 mB of the matching molten metal after sufficient heating. The tank holds 2880 mB, with no mixing until empty. Contents, heat, progress and fuel are saved; no GUI or chat feedback is used.

**Small** — 3x3x4 and 29 bricks + hatch, with an optional hollow hearth. Two automatically formed ports: item input (lower left) and fluid output (upper right). The item-input capability has slot 0 for raw metal and slot 1 for solid fuel. You can pipe molten metal OUT to other Create tanks and pipes. It does **not** accept fluids, export ingots, or cast ingots into items.

**Large** — 5x5x7, full seven-layer pattern. Four automatically formed ports: all four item and fluid ports at layer 2. Item inlet exposes the same two slots; item output automatically casts a hot ingot when extraction is requested. Its fluid inlet accepts registered molten iron/copper/gold without mixing, and its fluid outlet pumps them out. Empty-hand right click item output can take a hot ingot. See BLUEPRINTS.md in the package root.

Both variants connect through the NeoForge ItemHandler and FluidHandler block capabilities, which Create's funnels and pumps can query on the visible outward face of each port. These are *pipe-only* molten fluids; no pourable buckets/world source blocks were added.

Welding is server-controlled and independent of Create Super Glue. Forming a furnace changes only its marked side bricks into colored arrow ports; unwelding converts them back to Fireclay Bricks. The hatch persists its scale so the appropriate pattern is used after world reload.

Smoke emerges from the opening while burning. Molten metal becomes visible inside the chamber and causes Survival damage if stepped into when hot. Create Goggles show heat, contents and remaining burn state while looking at an assembled hatch. World saves should be backed up before installing a new test build.
