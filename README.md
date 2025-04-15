# Description

This is a Sublime Text 4 package that displays info about the currently selected character in the status bar. It displays the character itself, Unicode code point, and the character's name.

Names from [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) are supported (as obtained from [this file](https://github.com/ryanoasis/nerd-fonts/blob/master/glyphnames.json)). This can be easily disabled as outlined below if you don't need it.

# Commands & Config

The package comes with four commands, all prefixed with "Character Info:". 
asdasdasd
"Toggle Prefix", "Toggle Padding", and "Toggle Caps" are simply shortcuts to update the configuration.

"Character Info: Rebuild Nerdfonts Mappings" parses the glyphnames.json into a new file for the plugin to reference. 
If the glyphnames.json is outdated, it does not get updated. You'll need to navigate to the package directory and replace it with a new one from the link above (alternatively, just open an issue and I'll update the repo ASAP).

There are only a few config options: 
- "enable_prefix", which enables the "U+" prefix for the code point display.
- "enable_padding", which adds extra zeroes to the start of the code point (take "m" for example, this brings the code point from just "6D" to "006D").
- "capitalize", capitalizes letters in the code points, for example instead of "U+0d9e" you see "U+0D9E".
- "right_of_cursor", this option, off by default, will cause the plugin to process the character to the right of the cursor, as opposed to the one to the left.
- "nerdfonts_support" can be used to disable support for Nerd Fonts characters. The names will default to "None". No performance impact either way, so I'm not sure why you'd want this, but you deserve the option.
