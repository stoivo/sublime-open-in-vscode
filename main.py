import sublime
from sublime_plugin import WindowCommand

import subprocess
import os
from functools import partial

from itertools import chain
flatten = chain.from_iterable

# code --new-window --add ~/dev/work/repo/
# code --reuse-window --goto ~/dev/work/repo/src/views/Departments.vue

first_time = False

def open_in_vs_code(path, folders):
    global first_time

    settings = sublime.load_settings("VSCode.sublime-settings")
    cmd = [settings.get('vscode-path')]

    if first_time:
        cmd.append('--new-window')

    for folder in folders:
        cmd.append("--add \"{}\"".format(folder))

    cmd.append('--reuse-window')

    if path:
        cmd.append('--goto')
        cmd.append('{}'.format(path))

    startupinfo = None
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(
        args=" ".join(cmd),
        startupinfo=startupinfo,
        shell=True,
        stdin=subprocess.PIPE,   # python 3.3 bug on Win7
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )


class VscOpenInVisalStudioCodeCommand(WindowCommand):
    def run(self):
        global first_time

        folders = self.window.folders() or []
        view = self.window.active_view()

        path = view.settings().get("git_savvy.file_path") or view.file_name()
        if path:
            sel = view.sel()
            if sel:
                (row, col) = view.rowcol(sel[0].a)
                open_in_vs_code('{}:{}:{}'.format(path, (row) + 1, col + 1), folders)
            else:
                open_in_vs_code(path, folders)
        else:
            open_in_vs_code(None, folders)


def get_subjects(view, *sections):
    # type: (sublime.View, str) -> Iterable[sublime.Region]
    return flatten(
        view.find_by_selector(
            'meta.git-savvy.status.section.{} meta.git-savvy.status.subject'.format(section)
        )
        for section in sections
    )


def region_as_tuple(region):
    # type: (sublime.Region) -> Tuple[int, int]
    return region.begin(), region.end()


def region_from_tuple(tuple_):
    # type: (Tuple[int, int]) -> sublime.Region
    return sublime.Region(*tuple_)


def unique_regions(regions):
    # type: (Iterable[sublime.Region]) -> Iterator[sublime.Region]
    # Regions are not hashable so we unpack them to tuples,
    # then use set, finally pack them again
    return map(region_from_tuple, set(map(region_as_tuple, regions)))


def unique_selected_lines(view):
    # type: (sublime.View) -> List[sublime.Region]
    return list(unique_regions(flatten(view.lines(s) for s in view.sel())))


def get_selected_subjects(view, *sections):
    # type: (sublime.View, str) -> List[str]
    selected_lines = unique_selected_lines(view)
    return [
        view.substr(subject)
        for subject in get_subjects(view, *sections)
        if any(line.contains(subject) for line in selected_lines)
    ]


def get_selected_files(view, base_path, *sections):
    # type: (sublime.View, str, str) -> List[str]
    if not sections:
        sections = ('staged', 'unstaged', 'untracked', 'merge-conflicts')

    make_abs_path = partial(os.path.join, base_path)

    return [
        os.path.normpath(make_abs_path(filename))
        for filename in get_selected_subjects(view, *sections)
    ]


class VscOpenInVisalStudioCodeGitSavvyStatusCommand(WindowCommand):
    def repo_path(self):
        view = self.window.active_view()
        settings = view.settings()
        return settings.get('git_savvy.repo_path')

    def run(self):
        folders = self.window.folders() or []
        view = self.window.active_view()

        for fpath in get_selected_files(view, self.repo_path()):
            open_in_vs_code(fpath, folders)
