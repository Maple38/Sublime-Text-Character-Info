import sublime_plugin
import sublime
import json
import unicodedata
import os

#   

settings_file = "character_info.sublime-settings"


def parse_glyphnames():
    with open(os.path.join(file_dir, "glyphnames.json")) as file_in:
        data_in = json.load(file_in)
        data = {}
        for key_old, val in data_in.items():
            key_new = val.get("code")
            if key_new:
                data[key_new] = key_old
            else:
                print(f"No 'code' value found at {key_old}, skipping...")

    with open(nerdfonts_ids_path, "w") as file_out:
        json.dump(data, file_out)


def get_char(view):
    if right_of_cursor:
        pos = view.sel()[0].a
    else:
        pos = view.sel()[0].a - 1

    char = view.substr(pos)

    id_int = ord(str(char))
    if enable_caps: code = format(id_int, "X")
    else: code = format(id_int, "x")

    return char, code, id_int


def settings_refresh():
    global settings
    settings = sublime.load_settings(settings_file)

    global \
        enable_prefix, \
        enable_padding, \
        enable_caps, \
        right_of_cursor, \
        nerdfonts_support
    enable_prefix = settings.get("enable_prefix")
    enable_padding = settings.get("enable_padding")
    enable_caps = settings.get("enable_caps")
    right_of_cursor = settings.get("right_of_cursor")
    nerdfonts_support = settings.get("nerdfonts_support")



def parse_name(char, code):
    try:
        return unicodedata.name(char)
    except ValueError:
        try:
            return mappings[code]
        except KeyError:
            return None


def load_mappings():
    if nerdfonts_support:
        print('Nerdfonts enabled.')
        global mappings
        try:
            with open(nerdfonts_ids_path, 'r') as file_in:
                mappings = json.load(file_in)
        except FileNotFoundError:
            parse_glyphnames()
            with open(nerdfonts_ids_path, 'r') as file_in:
                mappings = json.load(file_in)
    else:
        print('Nerdfonts disabled.')


class UnicodeInfo(sublime_plugin.EventListener):
    def on_selection_modified_async(self, view):
        if len(view.sel()) == 1 and view.sel()[0].empty():
            char, code, id_int = get_char(view)

            char_name = parse_name(char, code)

            if enable_padding:
                code = code.zfill(4)
            if enable_prefix:
                code = "U+" + code

            if not char.isprintable():
                char = repr(char)
            else:
                char = "'" + char + "'"

            output_string = f"Character: {char}, Unicode: {code}, Int: {id_int}, Name: {char_name}"
            # print(output_string)
            view.set_status("unicode", output_string)


class CharinfoRebuildNerdfontsMappings(sublime_plugin.ApplicationCommand):
    def run(self):
        parse_glyphnames()
        load_mappings()


class CharinfoTogglePrefix(sublime_plugin.ApplicationCommand):
    def run(self):
        val = settings.get("enable_prefix")
        settings.set("enable_prefix", not val)
        sublime.save_settings(settings_file)
        settings_refresh()


class CharinfoTogglePadding(sublime_plugin.ApplicationCommand):
    def run(self):
        val = settings.get("enable_padding")
        settings.set("enable_padding", not val)
        sublime.save_settings(settings_file)
        settings_refresh()


class CharinfoToggleCaps(sublime_plugin.ApplicationCommand):
    def run(self):
        val = settings.get("enable_caps")
        settings.set("enable_caps", not val)
        sublime.save_settings(settings_file)
        settings_refresh()


file_dir = os.path.dirname(__file__)
nerdfonts_ids_path = os.path.join(file_dir, "nerdfonts_ids.json")
settings_refresh()
load_mappings()
