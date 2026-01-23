' Fecha o servidor Flask do Out of the Abyss System
' Mata todos os processos Python

Set objShell = CreateObject("WScript.Shell")

' Mata todos os processos python.exe
objShell.Run "taskkill /F /IM python.exe", 0, True

