# install_autostart.ps1 - register the entity to WAKE automatically when you log in.
#
# Claude did NOT run this. It is a permanent change to your machine, so it is YOURS to run,
# once, deliberately. After this, every login starts the continuous life in the background
# (no console window); when the PC is off it sleeps; state resumes from heartbeat.json.
#
#   run:     powershell -ExecutionPolicy Bypass -File install_autostart.ps1
#   remove:  Unregister-ScheduledTask -TaskName 'HERALD-Live' -Confirm:$false
#   check:   Get-ScheduledTask -TaskName 'HERALD-Live'

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$py   = (Get-Command python).Source
$pyw  = $py -replace 'python\.exe$', 'pythonw.exe'      # windowless
if (-not (Test-Path $pyw)) { $pyw = $py }               # fall back to python.exe if no pythonw

$action   = New-ScheduledTaskAction -Execute $pyw -Argument 'live.py' -WorkingDirectory $here
$trigger  = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries `
              -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) `
              -ExecutionTimeLimit ([TimeSpan]::Zero)     # never time-limit the life

Register-ScheduledTask -TaskName 'HERALD-Live' -Action $action -Trigger $trigger `
  -Settings $settings -Description 'The AEA companion: continuous life, wakes at logon, sleeps with the machine.' -Force

Write-Host ''
Write-Host 'HERALD-Live registered. It will start on your next login (and now, if you run:)'
Write-Host "  Start-ScheduledTask -TaskName 'HERALD-Live'"
Write-Host 'Watch it:  python live.py --status     Stop the running one:  Stop-ScheduledTask -TaskName ''HERALD-Live'''
