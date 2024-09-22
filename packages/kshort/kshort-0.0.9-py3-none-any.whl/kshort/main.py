import argparse
import sys
from kshort.projects import get_projects
from kshort.selector import open_in_gnome_terminal, open_in_kitty, run
from kshort.utils import Config

def main():
    parser = argparse.ArgumentParser(description="Manage projects and kitty sessions.")
    parser.add_argument('--config-file', type=str, default='~/.config/projects_manager.json', help='Path to the config file')
    parser.add_argument('--list', action='store_true', help='List all projects')
    parser.add_argument('-g', action='store_true', help='Open in Gnome Terminal')

    args = parser.parse_args()
    config = Config.load(args.config_file)

    if args.list:
        projects = get_projects()
        for project in projects.values():
            print(project)
        sys.exit(0)

    selected_project = run(config)
    if selected_project:
        # print(f"Selected project: {selected_project.name}")
        if args.g:
            open_in_gnome_terminal(selected_project)
        else:
            open_in_kitty(selected_project)
    else:
        print("No project selected.")

if __name__ == "__main__":
    main()

