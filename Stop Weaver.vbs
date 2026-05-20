Option Explicit

Dim shell, fso, root, script

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

root = fso.GetParentFolderName(WScript.ScriptFullName)
script = root & "\stop-weaver.ps1"

shell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & script & """", 1, True
MsgBox "Weaver local app processes have been stopped.", 64, "Weaver"
