# Kshort
Kshort is a terminal script that allows you to search your projects from the terminal and open them in neovim, it currently works with kitty and gnome-terminal.

## Requirements
- `kitty` [terminal](https://sw.kovidgoyal.net/kitty/) | `gnome-terminal`
- `fzf` [repo](https://github.com/junegunn/fzf)
- `neovim`

## Installation

```shell
pip install kshort
```

## Configuration
Configure the projects in your director `~/.config/projects_manager.json`

- *File structure*
```json
{
  "directories": [
    {
      "name": "PHP",
      "directory": "~/code/php",
      "icon": " ",
      "color": "#5e79be"
    },
    {
      "name": "Javascript",
      "directory": "~/code/javascript/",
      "icon": " ",
      "color": "#ecb75d"
    }
  ],
  "projects": [
    {
      "name": "Neovim",
      "directory": "~/.config/nvim",
      "icon": " ",
      "color": "#509a3a"
    },
    {
      "name": "Awesome",
      "directory": "~/.config/awesome",
      "icon": " ",
      "color": "#535d6c"
    }
  ]
}
```

## Commands

- `kshort` list your projects in fzf and open them in kitty and using neovim
- `kshort -g` list your projects in fzf and open them in gnome-terminal and using neovim
- `kshort --list` returns a list of your configured projects
