
$DEFAULT_PY_VERSION = "3.13"
$GH_BRANCH = "main"
$GH_URL = "https://raw.githubusercontent.com/liquidcarbon/puppy/$GH_BRANCH/"
$PIXI_INSTALL_URL = "https://pixi.sh/install.ps1"

function Main {
    $DIR = Get-Location
    $global:PIXI_TOML = ""
    $global:PUP = ""
    while ($DIR -ne [System.IO.Path]::GetPathRoot($DIR)) {
        if (Test-Path "$DIR\pixi.toml") {
            $global:PIXI_TOML = "$DIR\pixi.toml"
        }
        if (Test-Path "$DIR\pup.py") {
            $global:PUP = "$DIR\pup.py"
            $global:PUP_HOME = $DIR
            break
        }
        $DIR = Split-Path $DIR
    }
    if ($args.Count -gt 0) {
        if ($PUP -and $args[0] -ne "update") {
            Run @args
        } elseif ($PUP -and $args[0] -eq "update") {
            Update
        } else {
            Install @args
        }
    } else {
        if ($PUP) {
            Run $null # make PS happy
        } else {
            Install $null
        }
    }
}

function Run {
    $PY = "$PUP_HOME\.pixi\envs\default\python.exe"
    if (Test-Path $PY) {
        & "$PY" "$PUP" @args
    } else {
        pixi run python "$PUP" @args
    }
}

function Update {
    Get-Pixi
    pixi self-update
    Pixi-Init
    Get-Python-UV-Click $null
    pixi update
    Get-Pup
}

function Install {
    if ((Get-ChildItem | Measure-Object).Count -gt 0) {
        $response = Read-Host -Prompt "$(Get-Location) is not empty; do you want to make it puppy's home? (y/n)"
        if ($response -ne "y") { exit 1 }
    }
    Get-Pixi
    Pixi-Init
    if ($args.Count -gt 0) {
        Get-Python-UV-Click $args[0]
    } else {
        Get-Python-UV-Click $null  # make PS 5 happy
    }
    Get-Pup
}

function Get-Pixi {
    if (-not (Get-Command pixi -ErrorAction SilentlyContinue)) {
        iwr -useb  $PIXI_INSTALL_URL | iex
        $env:PATH = "$HOME\.pixi\bin;" + $env:PATH  # new installs need this
        Write-Host "✨ $(pixi -V) installed"
    } else {
        Write-Host "✨ $(pixi -V) found"
    }
    $global:PIXI_HOME = Split-Path (Get-Command pixi).Source
}

function Pixi-Init {
    if ($PIXI_TOML -ne "") {
        Write-Host "✨ here be pixies! pixi.toml found"
    } else {
        pixi init .
        $global:PIXI_TOML = (Resolve-Path pixi.toml).Path
    }
}

function Py-Ver-Prompt {
    $PromptMessage = "Enter desired base Python version (supported: 3.9|3.10|3.11|3.12|3.13; blank=3.12)"
    $PY_VERSION = Read-Host -Prompt $PromptMessage
    if (-not $PY_VERSION) { $PY_VERSION = $DEFAULT_PY_VERSION }
    return $PY_VERSION
}

function Get-Python-UV-Click {
    param([string]$version)
    if ($version) {
        $PY_VERSION = $version
        $INSTALL = 1
    } else {
        if (Select-String -Path $PIXI_TOML -Pattern "python") {
            $INSTALL = 0
        } else {
            $PY_VERSION = Py-Ver-Prompt
            $INSTALL = 1
        }
    }
    if ($INSTALL -eq 1) {
        pixi add "python=$PY_VERSION"
        pixi add "uv>=0"
        Write-Host "🟣 $(pixi run uv --version)"
        pixi add "click>=8"
        # using ">=" overrides pixi's default ">=,<" and allows updates to new major versions
    } else {
        Write-Host "🐍 python lives here!"
    }
    pixi run python -VV
}

function Get-Pup {
    if ($PUP -ne "") {
        Invoke-WebRequest -Uri "$GH_URL/pup.py" -OutFile "$PUP"
    } else {
        Invoke-WebRequest -Uri "$GH_URL/pup.py" -OutFile "pup.py"
    }
    Invoke-WebRequest -Uri "$GH_URL/pup.ps1" -OutFile "$PIXI_HOME/pup.ps1"
    & "$PIXI_HOME/pup" hi
}

Main @args
