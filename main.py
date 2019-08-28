from sublime_plugin import WindowCommand
import os
# code --new-window --add ~/dev/work/snotra/repo_client_vue/
# code --reuse-window --goto ~/dev/work/snotra/repo_client_vue/src/views/Departments.vue

first_time = False


class VscOpenInVisalStudioCodeCommand(WindowCommand):
    def run(self):
        global first_time

        window = self.window
        folders = window.folders()
        code_path = "/usr/local/bin/code"
        view = window.active_view()
        path = view.file_name()
        sel = view.sel()
        print(sel[0])
        print(sel[0].a)
        print(view.rowcol(sel[0].a))
        (row, col) = view.rowcol(sel[0].a)

        cmd = [
            code_path,
            '--new-window' if first_time else '',
            '{}'.format(" ".join('--add ' + folder for folder in folders)) if folders else '',
            '--reuse-window',
            '--goto "{}:{}:{}"'.format(path, row + 1, col + 1) if path else None
        ]
        print((cmd))
        myCmd = " ".join(cmd)
        print(myCmd)
        os.system(myCmd)

