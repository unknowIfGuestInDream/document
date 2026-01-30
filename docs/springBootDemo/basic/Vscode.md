> 本文主要记录VSCode的设置

## settings.json
```json
{
    "workbench.colorTheme": "GitHub Dark Dimmed",
    "github.copilot.nextEditSuggestions.enabled": true,
    "java.configuration.maven.userSettings": "C:\\work\\env\\maven\\settings.xml",
    "java.configuration.maven.globalSettings": "C:\\work\\env\\maven\\settings.xml",
    "java.configuration.runtimes": [
        {
            "name": "JavaSE-21",
            "path": "C:\\work\\env\\jdk\\jdk21.0.9_10",
            "default": true
        },
        {
            "name": "JavaSE-17",
            "path": "C:\\work\\env\\jdk\\jdk-17.0.17+10"
        },
        {
            "name": "JavaSE-25",
            "path": "C:\\work\\env\\jdk\\jdk-25.0.1+8"
        }
    ],
    "files.autoSave": "afterDelay",
    "maven.executable.path": "C:\\work\\env\\maven\\apache-maven-3.9.12",
    "maven.settingsFile": "C:\\work\\env\\maven\\settings.xml",
    "maven.excludedFolders": [
        "**/target",
        "**/node_modules"
    ],
    "java.compile.nullAnalysis.mode": "automatic",
    "maven.pomfile.autoUpdateEffectivePOM": true,
    "maven.view": "hierarchical",
    "window.newWindowProfile": "默认",
    "editor.bracketPairColorization.independentColorPoolPerBracketType": true,
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.detectIndentation": false,
    "editor.fontLigatures": true,
    "editor.formatOnPaste": true,
    "editor.formatOnSave": true,
    "editor.guides.bracketPairs": true,
    "explorer.incrementalNaming": "smart",
    "editor.mouseWheelZoom": true,
    "editor.rulers": [
        120
    ],
    "editor.quickSuggestions": {
        "strings": "on",
        "comments": "on"
    },
    "editor.renderWhitespace": "boundary",
    "editor.smoothScrolling": true,
    "editor.wordWrap": "on",
    "editor.wordWrapColumn": 120,
    "explorer.confirmDelete": false,
    "explorer.confirmDragAndDrop": false,
    "explorer.fileNesting.enabled": true,
    "window.closeWhenEmpty": true,
    "window.dialogStyle": "custom",
    "window.newWindowDimensions": "inherit",
    "workbench.commandPalette.preserveInput": true,
    "workbench.editor.scrollToSwitchTabs": true,
    "workbench.startupEditor": "readme",
    "security.workspace.trust.untrustedFiles": "open",
    "problems.showCurrentInStatus": true,
    "telemetry.telemetryLevel": "error",
    "terminal.external.linuxExec": "bash",
    "terminal.integrated.confirmOnExit": "hasChildProcesses",
    "terminal.integrated.copyOnSelection": true,
    "terminal.integrated.enableVisualBell": true,
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "overrideName": true,
            "icon": "terminal-powershell",
            "args": [
                "-NoLogo"
            ]
        },
        "Command Prompt": {
            "path": [
                "${env:windir}\\Sysnative\\cmd.exe",
                "${env:windir}\\System32\\cmd.exe"
            ],
            "args": [],
            "icon": "terminal-cmd"
        },
        "Git Bash": {
            "source": "Git Bash",
            "icon": "terminal-git-bash"
        }
    },
    "terminal.integrated.smoothScrolling": true,
    "git.autofetch": true,
    "git.confirmSync": false,
    "git.enableSmartCommit": true,
    "git.mergeEditor": true,
    "merge-conflict.autoNavigateNextConflict.enabled": true,
    "npm.enableRunFromFolder": true,
    "npm.scriptExplorerAction": "run",
    "markdown.validate.enabled": true,
    "github.copilot.enable": {
        "plaintext": true,
        "markdown": true,
        "scminput": true
    },
}
```