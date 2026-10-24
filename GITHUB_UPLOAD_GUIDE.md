## Optional Welder appearance selection

Before publishing, choose the item appearance by double-clicking
`USE-2D-WELDER.cmd` or `USE-3D-WELDER.cmd` in the `Source` folder. The
publisher will include your selected model, and all offline asset checks
accept either mode. No gameplay classes or multiblock definitions change.

See `docs/WELDER_MODEL_SWITCH.md` for the optional resource-pack alternative.

---

# Push the V24 Welder update to GitHub (Windows)

Repository: https://github.com/BlazyXEET/Create-industrial

This package is **newer than GitHub main**. Do not copy GitHub main over the
package. Use the included script to publish the newer source into a **new
branch**, preserving GitHub main for review and merge.

## Requirements

- Windows 10/11 with Git for Windows installed and signed into an account
  allowed to push to `BlazyXEET/Create-industrial`.
- JDK **21** available in PowerShell (`java -version`).
- Python 3 (`py -3 --version` or `python --version`).
- Network connectivity to Gradle, NeoForge and Create dependency repositories.
- The **entire ZIP extracted**, not individual files pulled out of it.
- A backup of your Minecraft world before testing.

## Quick start

1. Extract `CreateIndustrial-V24-Welder-GitHub-Ready.zip` using Windows Explorer.
2. Open the extracted `Source` folder.
3. Easiest option: double-click `PUSH-WELDER-TO-GITHUB.cmd`. It runs all
   checks and pushes a new branch only when every required check succeeds.
   Alternatively, in the folder address bar type `powershell` and press Enter
   to use the commands below.
4. Review what would be uploaded (no build, commit or push):

   `powershell -NoProfile -ExecutionPolicy Bypass -File .\Publish-Welder-To-GitHub.ps1 -PreviewOnly`

   Preview creates a local folder called `CreateIndustrial-GitHub-Publish` beside
   `Source`. Delete that preview folder or choose a different `-Destination`
   before running the next command.
5. Publish the new feature branch **only after all checks pass**:

   `powershell -NoProfile -ExecutionPolicy Bypass -File .\Publish-Welder-To-GitHub.ps1 -Push`

   This clones fresh, creates a new unique branch name, runs all offline tests,
   compiles with `gradlew.bat clean build`, runs `runGameTestServer`, makes a
   commit and pushes that branch. A failed check stops the process before push.

   **CI-only alternative:** If your computer cannot download Gradle, you can
   intentionally push a NEW, explicitly unverified branch for GitHub Actions:

   `powershell -NoProfile -ExecutionPolicy Bypass -File .\Publish-Welder-To-GitHub.ps1 -Push -CIOnly`

   CI-only still requires offline checks to pass. It deliberately skips local
   compilation/GameTests and MUST NOT be merged or called playable until the
   GitHub Actions build and Minecraft tests pass. This is the only opt-in
   bypass, and it never force-pushes or updates main.

6. Follow the printed GitHub compare link and open a pull request. Review the
   diff; merge to main only after the Minecraft tests and player checks pass.

The script NEVER force-pushes and NEVER updates main directly. It replaces the
**new branch's** old `src`, `tests`, `tools`, `docs`, `art`, and `gradle`
directories with the corresponding verified package sources. It will not
remove your existing upstream main branch, but the PR may show large diffs.

## Troubleshooting

- If `git` is missing, install Git for Windows.
- If `java -version` is not 21, set `JAVA_HOME` to your JDK 21 installation.
- If Gradle fails while downloading, check Internet, firewall and proxy/DNS;
  do not bypass compilation by uploading an older JAR under a new name.
- If Git says `Author identity unknown`, configure `git config --global
  user.name "Your Name"` and `git config --global user.email "your@email"`
  using your own values. Do not paste credentials or tokens into the script.
- If push is denied, check access to the repository or use a personal fork.
- If GameTests fail, do not publish as verified. Use the logs to fix the mod.
- If a preview run left a destination folder, remove it before the publishing
  run or pass `-Destination C:\your\new\unused\path`.

## Manual safety checks after CI

1. Minecraft loads with the target NeoForge and Create dependencies.
2. Welder in main hand is oriented correctly in first/third person.
3. Small furnace builds/welds in four rotations and supported hollow variants.
4. Large furnace builds/welds in four rotations.
5. Shift+right-click and Shift+left-click remove welds.
6. Breaking a casing unwelds without duplicating or deleting stored materials.
7. Reassembly and world reload preserve state.
8. Complete game test server and multiplayer tests before public release.

To add more weldable machines, read `docs/ADDING_MACHINES.md` and use
`PatternMachineDefinition`. No edits to the Welder input handlers are needed.
