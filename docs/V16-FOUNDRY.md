# V16 foundry operation

Historical V16 guide. For the current steelmaking route, use V17-FOUNDRY.md
and V17-REFINING.md; V17 removes the steel mixing shortcuts described below.

Minecraft 1.21.1 / NeoForge 21.1.257 / Create 6.0.10-280 / Java 21.

This is a gameplay model of ironmaking and metal recycling. It represents air blast,
refractory heat storage, ore reduction, flux, slag and tapping. It does not calculate
real chemical equilibrium, gas pressure or a full temperature gradient.

## Building and starting either furnace

Use the existing 3x3x4 small or 5x5x7 large blueprint and assemble it with the Welder.
The large blueprint's originally unspecified foundation row remains air. Keep the
central chimney and three blocks above its outlet clear. All four horizontal
orientations remain supported.

The controller face is also the air inlet. Place a Create Encased Fan 1–4 blocks
directly in front of it, blowing toward the controller, with a clear air path.
Power it at 64 RPM or more. If it sucks air away, reverse its rotation. A survival
water wheel/gearbox drive works; creative motors are used only in automated tests.

Insert material, fuel and flux through the item inlet, or right-click the hatch
with the corresponding item. Input slot 0 is material, 1 fuel, and 2 flux.
Calcite and Create limestone are accepted fluxes. Each block supplies 16 charges.
Coal, charcoal, coal blocks, blaze rods and the new coke are supported fuels.
Coke is made by heated Create mixing of two coal and burns for 3200 ticks.

Natural draft heats to about 1100 C. Forced draft can reach 1700 C. The larger
refractory mass heats more slowly and retains heat longer. A sealed chimney
prevents new fuel ignition and processing. Fuel already burning continues to
burn; there is no instant fuel refund or infinite ignition trick.

## Ore reduction and melting

Raw iron becomes **pig iron**, not finished steel. Ore reduction requires the air
blast, at least 1200 C (or the metal's higher melting point), and sufficient flux.
One raw metal gives 144 mB of metal and 36 mB of slag; a raw storage block gives
nine times those amounts. Flux is consumed only by reduction, not recycling.

Aluminium requires its alumina/refining route first. Uranium raw material is not
accepted for carbon reduction in this furnace. Refined aluminium, uranium and
other registered metals can be remelted. One ingot is 144 mB, one nugget 16 mB,
and one storage block 1296 mB. Blocks take nine times the ingot processing time.
Changing the input item resets progress; a temporary heat or output shortage
pauses the same charge. Progress, heat, inventory, flux and slag survive reload.

Pig iron can be refined into steel in a heated Create basin with calcite. This
is an accessible abstraction of refining, not a literal oxygen-converter model.
The previous superheated iron/charcoal steel recipe remains available.

## Tapping, cooling and automation

The small furnace holds 2880 mB of metal; the large holds 11520 mB. Each has a
separate slag reservoir of the same capacity. Full reservoirs stop ore processing
without deleting the charge. Different metals cannot share the metal reservoir.

Both sizes expose metal and slag through the existing fluid output port. Use
Create Smart Fluid Pipes with filters and separate receiving tanks. Unfiltered
draining prefers metal, then slag; do not expect one tank to mix the fluids.
Slag can flow at 1000 C or hotter. The large furnace also retains its fluid input
and item output; its item output casts ingots. The small remains fluid-output
only, with no added item output or fluid input.

For the small furnace, send metal to a Create basin under a Mechanical Press.
Every registered molten metal has a 144 mB-to-one-ingot compacting/casting recipe.
This also provides a complete automatic pig-iron-to-steel route without needing
the large furnace just to obtain a solid ingot.

Create basin compacting turns 144 mB slag into one slag piece. Slag can replace
part of the aggregate in reinforced concrete, giving the byproduct a use.
Slag crust patches appear on the visible molten pool and disappear when tapped.
The large furnace shows a full 3x3 pool. Its edge cells share the same authoritative
heat/damage checks and remain present across scheduled surface cleanup ticks.

Cold stored metal stays in the hearth and must be reheated before it can flow.
Incoming hot fluid contributes heat in proportion to its amount; 1 mB cannot
instantly heat an entire cold furnace. Fuel is not replaced while a reservoir
is blocked, and unnecessary new fuel ignition pauses near the draft temperature
limit. Engineer's Goggles show actual heat, draft, exhaust, flux, slag and charge
progress, including what currently prevents processing.

## Scope and remaining checks

The multiblock designs, Welder selection/undo and existing pipe directions are
preserved. No GUI, custom bucket or additional dependency is introduced.
An oversized stored charge prevents converting a large controller to the smaller
furnace; drain it first so a resize cannot discard stored metal or slag.
Plutonium remains an intentionally abstract late-game Create transmutation
recipe; no real nuclear reactor or plutonium ore is claimed.

Automated tests are separate from visual client playtesting and a full two-player
factory test. Consult the bundled verification report for the checks actually run.

Engineering references: British Steel, “How we make steel”; USGS, “Iron and Steel
Slag Statistics and Information”; World Steel Association, “Raw materials.”
