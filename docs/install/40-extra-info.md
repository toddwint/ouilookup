# Extra Info

## `oui.csv` and `oui.json` files

The program needs to download a file and convert it to JSON format to perform the lookups. The location of these files are:

- Linux
    - `$HOME/.local/share/${script}/oui.csv`
    - `$HOME/.local/share/${script}/oui.json`
- MacOS
    - `$HOME/.local/share/${script}/oui.csv`
    - `$HOME/.local/share/${script}/oui.json`
- Windows
    - `%appdata%/${script}/oui.csv`
    - `%appdata%/${script}/oui.json`

This folder is not automatically removed on program uninstallation. You can manually delete it without issues.


## Shell Completions

This program includes shell completions which should be installed by default to your local user's share directory (e.g. `$HOME/.local/share`).

  - `bash`
    - `$HOME/.local/share/bash-completion/completions/${script}`
  - `zsh`
    - `$HOME/.local/share/zsh/site-functions/_${script}`
  - `fish`
    - `$HOME/.local/share/fish/vendor_completions.d/${script}.fish`

If shell completions are not working, this program includes an option to provide the shell completion to stdout.

Run the command:

```sh
${script} --completion <shell>
```

Where `<shell>` is the name of your shell.

Using shell redirection you can place these commands in a file where your shell looks for shell completions. This part you will have to research for your shell.
