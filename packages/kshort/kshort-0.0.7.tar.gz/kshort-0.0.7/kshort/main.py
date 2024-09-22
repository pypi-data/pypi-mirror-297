import argparse
import os
import sys
from kshort.projects import get_projects, remove_item, remove_cache
from kshort.selector import open_in_kitty, run
from kshort.utils import Config

def add_binding_to_kitty(project):
    kitty_config_path = os.path.expanduser("~/.config/kitty/kitty.conf")

    if not os.path.exists(kitty_config_path):
        print(f"Kitty config file not found at {kitty_config_path}")
        return

    with open(kitty_config_path, 'a') as config_file:
        binding_command = f"map cmd+{project.name[0].upper()} spawn {project.get_command()}\n"
        config_file.write(binding_command)
        print(f"Binding added: cmd+{project.name[0].upper()} -> {project.get_command()}")


def main():
    parser = argparse.ArgumentParser(description="Manage projects and kitty sessions.")
    parser.add_argument('--config-file', type=str, default='~/.config/projects_manager.json', help='Path to the config file')
    parser.add_argument('--bind', type=str, help='Bind a project to a key')
    parser.add_argument('--forget', type=str, help='Forget a project')
    parser.add_argument('--list', action='store_true', help='List all projects')
    parser.add_argument('--remove-cache', action='store_true', help='Remove cache file')

    args = parser.parse_args()
    config = Config.load(args.config_file)

    if args.remove_cache:
        remove_cache()
        sys.exit(0)

    if args.list:
        projects = get_projects()
        for project in projects.values():
            print(project)
        sys.exit(0)

    if args.bind:
        # Bind functionality (e.g., create a key binding in Kitty or another application)
        projects = get_projects()
        print(projects)
        project = projects.get(args.bind)
        if project:
            add_binding_to_kitty(project)
        else:
            print(f"Project '{args.bind}' not found.")
        sys.exit(0)

    if args.forget:
        remove_item(args.forget)
        sys.exit(0)

    selected_project = run(config)
    if selected_project:
        # print(f"Selected project: {selected_project.name}")
        open_in_kitty(selected_project)
    else:
        print("No project selected.")

if __name__ == "__main__":
    main()

