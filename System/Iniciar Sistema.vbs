' Launcher silencioso do Out of the Abyss System
' Executa o PowerShell script sem mostrar janela

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Pega o diretorio do script
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Executa o PowerShell oculto (0 = hidden)
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & strPath & "\run_system.ps1""", 0, False
