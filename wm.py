#!/usr/bin/env python3
import os, sys

# TODO: add cache
def get_icon(wm_class: str) -> str:
    from xdg import DesktopEntry, IconTheme

    env_XDG_DATA_DIRS = os.getenv("XDG_DATA_DIRS")
    if not env_XDG_DATA_DIRS:
        print("env XDG_DATA_DIRS not exist", file=sys.stderr)
        return ""

    xdg_app_dirs = []
    for dir in env_XDG_DATA_DIRS.split(":"):
        xdg_app_dirs.append(os.path.join(dir, "applications"))

    icon_name = None
    icon_name_Exec = None
    for dir in xdg_app_dirs:
        if not os.path.isdir(dir):
            continue
        for file in os.listdir(dir):
            if file.endswith(".desktop"):
                entry = DesktopEntry.DesktopEntry(os.path.join(dir, file))
                if wm_class.lower() in entry.getStartupWMClass().lower():
                    icon_name = entry.getIcon()
                    break
                if wm_class.lower() in entry.getExec().lower():
                    icon_name_Exec = entry.getIcon()
        if icon_name:
            break
    if (not icon_name) and icon_name_Exec:
        icon_name = icon_name_Exec

    if icon_name:
        return IconTheme.getIconPath(icon_name)
    else:
        print("not found", file=sys.stderr)
        return ""

def print_rofi_entry(id:str, wm_class:str, title:str) -> None:
    print("".join([
        id,
        "\0",
        "\x1f".join([
            "icon", get_icon(wm_class),
            "display", f"{wm_class:12} {title}",
            "meta", f"{wm_class} {title}",
        ]),
    ]))

import subprocess

# Output of `wmctrl -l`:
# window_id  num host title
# window_id  num host title
# ...
for line in subprocess.check_output(["wmctrl", "-l"]).decode("utf-8").splitlines():
    line_split = line.split(maxsplit=3)
    window_id = line_split[0]
    title = line_split[3]

    # Output of `xprop -id xxx WM_CLASS`:
    # WM_CLASS(STRING) = "Name", "WC_CLASS"）
    wm_class = subprocess.check_output(["xprop", "-id", window_id, "WM_CLASS"]).decode("utf-8").split('"')[3]
    if wm_class == "firefox":
        continue

    print_rofi_entry(window_id, wm_class, title)

# Output of `brotab list`:
# brotab_id   title
# brotab_id   title
# ...
for line in subprocess.check_output(["brotab", "list"]).decode("utf-8").splitlines():
    line_split = line.split(maxsplit=1)
    brotab_id = line_split[0]
    title = line_split[1]
    print_rofi_entry(brotab_id, "firefox", title)
