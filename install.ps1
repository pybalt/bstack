param(
    [ValidateSet("hermes", "claude", "codex", "cursor", "antigravity", "all")]
    [string]$Agent,
    [string]$Target,
    [ValidateSet("flat", "layered")]
    [string]$Layout,
    [string]$Zip,
    [string]$SkillsDir,
    [switch]$NoAdapter,
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ArgsList = @((Join-Path $ScriptDir "install.py"))

if ($Agent) { $ArgsList += @("--agent", $Agent) }
if ($Target) { $ArgsList += @("--target", $Target) }
if ($Layout) { $ArgsList += @("--layout", $Layout) }
if ($Zip) { $ArgsList += @("--zip", $Zip) }
if ($SkillsDir) { $ArgsList += @("--skills-dir", $SkillsDir) }
if ($NoAdapter) { $ArgsList += "--no-adapter" }
if ($Force) { $ArgsList += "--force" }
if ($DryRun) { $ArgsList += "--dry-run" }

python @ArgsList
exit $LASTEXITCODE
