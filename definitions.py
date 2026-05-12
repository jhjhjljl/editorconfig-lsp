PROPERTIES = {
    "indent_style": {
        "values": {"tab", "space"},
        "description": "Use tabs or spaces for indentation."
    },
    "indent_size": {
        "values": None,
        "description": "Number of columns per indentation level. Can be a whole number or 'tab' (uses tab_width)."
    },
    "tab_width": {
        "values": None,
        "description": "Number of columns for a tab character. Defaults to indent_size."
    },
    "end_of_line": {
        "values": {"lf", "cr", "crlf"},
        "description": "Line ending style. lf, cr, or crlf."
    },
    "charset": {
        "values": {"latin1", "utf-8", "utf-8-bom", "utf-16be", "utf-16le"},
        "description": "Character set encoding. utf-8-bom is discouraged."
    },
    "spelling_language": {
        "values": None,
        "description": "Natural language for spell checking. Format: 'en' or 'en-US'."
    },
    "trim_trailing_whitespace": {
        "values": {"true", "false"},
        "description": "Remove whitespace before newlines on save."
    },
    "insert_final_newline": {
        "values": {"true", "false"},
        "description": "Ensure file ends with a newline on save."
    },
    "root": {
        "values": {"true", "false"},
        "description": "Set to true to stop searching parent directories for .editorconfig files. Must be in the preamble, not inside a section."
    }
}
