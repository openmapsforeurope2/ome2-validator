# Sets up the environment variables
param (
    [string]$QgisPath,
    [switch]$UpdateEnvFile
)

# Helper functions
function GetWin32QgisDirs() {
    $candidates = Get-Item "$env:ProgramFiles\QGIS *" | Where-Object {Test-Path "$_/bin/qgis-bin.env"}
    $candidates | ForEach-Object {Add-Member -InputObject $_ -NotePropertyName 'Version' -NotePropertyValue (GetQgisVersionNumber $_)}
    return $candidates | Sort-Object -Property Version -Descending
}

function GetQgisVersionNumber($dir) {
    $ver = $dir.Name.Split(" ")[1]
    $major, $minor, $build = $ver.split('.')
    return [System.Tuple]::Create([int]$major, [int]$minor, [int]$build)
}

function ReadEnvFile([string]$path) {
    $res = [ordered]@{}
    Get-Content $path | ForEach-Object {
        $k, $v = $_ -split '=',2
        $res[$k] = $v
    }
    return $res;
}


# Param handling
if ([string]::IsNullOrEmpty($QgisPath)) {
    if ([System.Environment]::OSVersion.Platform -ne 'Win32NT') {
        throw 'Support for finding QGIS paths on Linux is missing'
    }
    else {
        $bestQgisDir = (GetWin32QgisDirs)[0]

        if ($null -eq $bestQgisDir) {
            throw 'Could not find a QGIS installation'
        }
        else {
            $QgisPath = $bestQgisDir.FullName
        }
    }
}

# Main logic
$vars = ReadEnvFile "$QgisPath/bin/qgis-bin.env"
$env:PYTHONHOME = $vars['PYTHONHOME']
$newPathPrefix = "$($vars['PATH']);"
if (-not $env:Path.StartsWith($newPathPrefix)) {
    $env:Path = "$($vars['PATH']);$env:Path"
}
else {
    Write-Host "Note: PATH env variable is already up to date"
}
$SEP = [System.IO.Path]::PathSeparator
$env:PYTHONPATH="$([System.IO.FileInfo]::new("$QgisPath/apps/qgis/python").FullName)$SEP$([System.IO.FileInfo]::new("$QgisPath/apps/qgis/python/plugins").FullName)"

if ($UpdateEnvFile) {
    Write-Output $env:PYTHONPATH | Set-Content .\.env
}
