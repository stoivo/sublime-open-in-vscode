## Visual Studio Code - sublime integration

This package lets you open Visual Studio Code from sublime. It's a very simple integration. It calls to the code executable with the path to the current file and directory.

I created this since there are cases where the VScode integration is better like TypeScript integration.

demo:
![demo](https://user-images.githubusercontent.com/3492040/74849506-12179c80-5339-11ea-879d-e78cab43cbb7.gif)

There are a default key binding and a command pallet command.
```json
[
  { "keys": ["ctrl+super+v", "ctrl+super+s"], "command": "vsc_open_in_visal_studio_code" },
]
```
