import sublime
from sublime_plugin import WindowCommand
import subprocess
import os

# code --new-window --add ~/dev/work/repo/
# code --reuse-window --goto ~/dev/work/repo/src/views/Departments.vue

first_time = False


class VscOpenInVisalStudioCodeCommand(WindowCommand):
    def run(self):
        global first_time

        window = self.window
        folders = window.folders() or []
        settings = sublime.load_settings("VSCode.sublime-settings")
        view = window.active_view()

        cmd = [
            settings.get('vscode-path'),
        ]

        if first_time:
            cmd.append('--new-window')

        for folder in folders:
            cmd.append("--add \"{}\"".format(folder))

        cmd.append('--reuse-window')

        path = view.file_name()
        sel = view.sel()

        if path:
            cmd.append('--goto')
            if sel:
                (row, col) = view.rowcol(sel[0].a)
                cmd.append('{}:{}:{}'.format(path, (row) + 1, col + 1))
            else:
                cmd.append('{}'.format(path))

        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.Popen(
            args=cmd,
            startupinfo=startupinfo,
            shell=True,
            stdin=subprocess.PIPE,   # python 3.3 bug on Win7
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
