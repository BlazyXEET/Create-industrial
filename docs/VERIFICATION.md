> **Historical verification document (V12–V14), not a V20 test report.** For V20 use [V20 seamless foundry](V20-SEAMLESS-FOUNDRY.md) and [latest offline checks](verification/offline-checks.txt).

# V12 verification boundary

- Source is based on audited upstream revision 9f04ad2110c4f2547b0a9fee676d794009345bc7 plus V11.
- The JDK 21 offline parser, six pure-Java tests, resource/texture validator and V12 static contracts are checked before packaging.
- Eleven Minecraft GameTests are included, including a new test for 4 formed ports, all outward capability faces, molten input/output, item casting and brick restoration after unweld.
- Full NeoForge compile, runGameTestServer, and client gameplay were **not executed** in the authoring environment (DNS cannot resolve Gradle, GitHub or dependency hosts). No runnable JAR is being represented as verified.
- Held Welder transforms, yellow outlines, smoke, Create pipe connection and goggles all require Minecraft client playtesting.
- The Windows builder only promotes a JAR after Gradle compile and all eleven GameTests succeed unless the user deliberately runs the build-only test script.

V14 adds ALT-air GameTest and requires compilation against NeoForge 21.1.257 / Create 6.0.10-280. Static passing checks do not establish client rendering correctness.
