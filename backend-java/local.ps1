param([ValidateSet('test','run')][string]$Action = 'test')
$ErrorActionPreference = 'Stop'
$jdkDirectory = Get-ChildItem "$PSScriptRoot\.tools\jdk" -Directory | Select-Object -First 1
$mavenDirectory = Get-ChildItem "$PSScriptRoot\.tools\maven" -Directory | Select-Object -First 1
if (!$jdkDirectory -or !$mavenDirectory) { throw 'Java e Maven portáteis não encontrados em .tools.' }
$env:JAVA_HOME = $jdkDirectory.FullName
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
Push-Location $PSScriptRoot
try {
    if ($Action -eq 'run') {
        if (!$env:DERMAPONTE_PASSWORD) { throw 'Defina DERMAPONTE_PASSWORD antes de iniciar.' }
        & "$($mavenDirectory.FullName)\bin\mvn.cmd" '-B' '-ntp' '-Dmaven.repo.local=.tools/repository' spring-boot:run
    } else {
        & "$($mavenDirectory.FullName)\bin\mvn.cmd" '-B' '-ntp' '-Dmaven.repo.local=.tools/repository' test
    }
    if ($LASTEXITCODE -ne 0) { throw 'Maven terminou com erro.' }
} finally { Pop-Location }
