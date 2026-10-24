#requires -Version 5.1
<#
  Copy this entire source project to a NEW, reviewable GitHub branch.
  Examples:
    .\Publish-Welder-To-GitHub.ps1 -PreviewOnly
    .\Publish-Welder-To-GitHub.ps1 -Push
  No force push or automatic merge is ever performed.
#>
[CmdletBinding()]
param(
    [string]$Repository = 'https://github.com/BlazyXEET/Create-industrial.git',
    [string]$BaseBranch = 'main',
    [string]$Branch = ('feature/welder-multiblock-' + (Get-Date -Format 'yyyyMMdd-HHmmss')),
    [string]$Destination = (Join-Path (Split-Path -Parent $PSScriptRoot) 'CreateIndustrial-GitHub-Publish'),
    [switch]$PreviewOnly,
    [switch]$CIOnly,
    [switch]$Push
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Run-Tool([string]$Executable, [string[]]$ToolArgs) {
    & $Executable @ToolArgs
    if ($LASTEXITCODE -ne 0) {
        throw "$Executable failed with exit code $LASTEXITCODE. Nothing was pushed."
    }
}

$source = $PSScriptRoot
foreach ($relative in @('src', 'gradlew.bat', 'build.gradle', 'tools/run_offline_checks.py')) {
    if (-not (Test-Path -LiteralPath (Join-Path $source $relative))) {
        throw "Not a valid extracted mod Source directory; missing: $relative"
    }
}
if ($PreviewOnly -and ($Push -or $CIOnly)) { throw 'PreviewOnly cannot be combined with Push or CIOnly.' }
if ($CIOnly -and -not $Push) { throw 'CIOnly must be combined with Push to start GitHub Actions.' }
if (Test-Path -LiteralPath $Destination) {
    throw "Destination already exists: $Destination. Choose -Destination with a new empty path."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required. Install Git for Windows, then reopen PowerShell.'
}
if (-not (Get-Command java -ErrorAction SilentlyContinue) -and -not ($PreviewOnly -or $CIOnly)) {
    throw 'Java 21 is required for the actual mod build.'
}

Write-Host 'Cloning the existing repository main branch...' -ForegroundColor Cyan
Run-Tool 'git' @('clone', '--branch', $BaseBranch, '--single-branch', $Repository, $Destination)
Run-Tool 'git' @('-C', $Destination, 'switch', '-c', $Branch)

# Replace only this mod's project-owned source directories IN THE NEW BRANCH.
# Old files from the upstream repository cannot silently shadow new Java
# classes/resources; upstream main itself remains untouched and recoverable.
foreach ($directory in @('src', 'tests', 'tools', 'docs', 'art', 'gradle')) {
    $old = Join-Path $Destination $directory
    if (Test-Path -LiteralPath $old) { Remove-Item -LiteralPath $old -Recurse -Force }
}
$omit = @('.git', '.gradle', '.idea', '.vscode', 'build', 'run', 'out', 'logs')
Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
    if ($_.Name -notin $omit) {
        Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
    }
}

Write-Host ''
Write-Host 'Review the incoming changes before publishing:' -ForegroundColor Cyan
Run-Tool 'git' @('-C', $Destination, 'add', '-A')
Run-Tool 'git' @('-C', $Destination, 'diff', '--cached', '--check')
Run-Tool 'git' @('-C', $Destination, 'diff', '--cached', '--stat')

if ($PreviewOnly) {
    Write-Host 'Preview complete. No build, commit, or push occurred.' -ForegroundColor Yellow
    Write-Host "Review the new branch at: $Destination"
    exit 0
}

Push-Location $Destination
try {
    Write-Host 'Running executable offline regression checks...' -ForegroundColor Cyan
    if (Get-Command py -ErrorAction SilentlyContinue) {
        Run-Tool 'py' @('-3', 'tools/run_offline_checks.py')
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        Run-Tool 'python' @('tools/run_offline_checks.py')
    } else {
        throw 'Python 3 is needed to run the offline regression suite.'
    }

    # These checks MUST pass before an automated push. Minecraft compilation
    # and GameTests were unavailable in the original authoring environment.
    if ($CIOnly) {
        Write-Warning 'CI-ONLY MODE: local Minecraft compilation and GameTests were NOT run.'
        Write-Warning 'The pushed branch is UNVERIFIED. GitHub Actions must pass before merging or installing.'
    } else {
        Write-Host 'Compiling the Minecraft/NeoForge/Create mod...' -ForegroundColor Cyan
        Run-Tool (Join-Path $Destination 'gradlew.bat') @('clean', 'build', '--no-daemon')
        Write-Host 'Running actual Minecraft GameTests...' -ForegroundColor Cyan
        Run-Tool (Join-Path $Destination 'gradlew.bat') @('runGameTestServer', '--no-daemon')
    }

    $name = & git -C $Destination config user.name
    $email = & git -C $Destination config user.email
    if ([string]::IsNullOrWhiteSpace($name) -or [string]::IsNullOrWhiteSpace($email)) {
        throw 'Configure git user.name and user.email before committing (git config --global ...).'
    }
    Run-Tool 'git' @('-C', $Destination, 'commit', '-m', 'Make Welder multiblocks extensible and preserve V23 model')
    if ($Push) {
        Write-Host 'Pushing ONLY the new feature branch...' -ForegroundColor Cyan
        Run-Tool 'git' @('-C', $Destination, 'push', '-u', 'origin', $Branch)
        Write-Host "Branch pushed: $Branch" -ForegroundColor Green
        Write-Host "Open a pull request at https://github.com/BlazyXEET/Create-industrial/compare/$BaseBranch...$Branch"
    } else {
        Write-Host 'Checks passed and local commit created. Nothing pushed yet.' -ForegroundColor Green
        Write-Host "To push later: git -C `"$Destination`" push -u origin $Branch"
    }
} finally {
    Pop-Location
}
