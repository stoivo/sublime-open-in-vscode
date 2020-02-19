import sublime
from sublime_plugin import WindowCommand
import os

# code --new-window --add ~/dev/work/repo/
# code --reuse-window --goto ~/dev/work/repo/src/views/Departments.vue

first_time = False


class VscOpenInVisalStudioCodeCommand(WindowCommand):
    def run(self):
        global first_time

        window = self.window
        folders = window.folders()
        settings = sublime.load_settings("VSCode.sublime-settings")
        view = window.active_view()
        path = view.file_name()
        sel = view.sel()
        (row, col) = view.rowcol(sel[0].a)

        cmd = [
            settings.get('vscode-path'),
            '--new-window' if first_time else '',
            '{}'.format(" ".join('--add ' + "'{}'".format(folder) for folder in folders)) if folders else '',
            '--reuse-window',
            '--goto "{}:{}:{}"'.format(path, (row) + 1, col + 1) if path else None
        ]
        myCmd = " ".join(cmd)
        os.system(myCmd)
