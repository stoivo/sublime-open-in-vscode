## Visual Studio Code - sublime integration

This package lets you open Visual Studio Code from sublime. It's a very simple integration. It calls to the code executable with the path to the current file and directory.

I created this since there are cases where the VScode integration is better like TypeScript integration.

demo:
![demo](https://user-images.githubusercontent.com/3492040/74849506-12179c80-5339-11ea-879d-e78cab43cbb7.gif)

There are a default key binding and a command pallet command.
```jsonb
[
  { "keys": ["ctrl+super+v", "ctrl+super+s"], "command": "vsc_open_in_visal_studio_code" },

  // There are some tool to open VScode from GitSavvy
  // Can highly recommend GitSavvy as git integration in Sublime

  // Open in vscode from GitSavvy inline diff
  {
    "keys": ["o"],
    "command": "vsc_open_in_visal_studio_code",
    "context": [
      { "key": "setting.command_mode", "operator": "equal", "operand": false },
      { "key": "setting.git_savvy.inline_diff_view", "operator": "equal", "operand": true }
    ]
  },
  // Open in vscode from GitSavvy status
  {
    "keys": ["o"],
    "command": "vsc_open_in_visal_studio_code_git_savvy_status",
    "context": [
      { "key": "setting.command_mode", "operator": "equal", "operand": false },
      { "key": "setting.git_savvy.status_view", "operator": "equal", "operand": true }
    ]
  },
]
```
