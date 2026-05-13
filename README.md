# editorconfig-lsp

This is my first LSP. Since `.editorconfig` has very little configuration, it was a tiny project, but I got to learn how LSP works without using a library.

It includes:
- Completion
- Hover
- Diagnostics

All standard features that an LSP provides.

## Installation

You can install it using:
```bash
pip3 install editorconfig-lsp
```

## Editor Setup

### Helix
For Helix, you can add this to your `languages.toml`:

```toml
[language-server.editorconfig-lsp]
command = "editorconfig-lsp"

[[language]]
name = "editorconfig"
scope = "source.editorconfig"
file-types = [{glob = ".editorconfig"}]
roots = []
language-servers = ["editorconfig-lsp"]
```

For other editors, you'll need to configure them to use the `editorconfig-lsp` command.
