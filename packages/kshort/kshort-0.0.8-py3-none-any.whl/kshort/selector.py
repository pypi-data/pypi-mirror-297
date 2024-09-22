import os
import glob
from kshort.project import Project
import subprocess

def run(config):
    projects = []

    if not config['directories'] or not config['projects']:
        print("No directories or projects found in the config.")
        return None

    for directory in config['directories']:
        expanded_dir = os.path.expanduser(directory['directory'])
        for file in glob.glob(os.path.join(expanded_dir, '*')):
            if os.path.isdir(file):
                projects.append(Project(
                    path=file,
                    name=os.path.basename(file),
                    group=directory.get('name'),
                    icon=directory.get('icon'),
                    color=directory.get('color')
                ))

    for proj in config['projects']:
        projects.append(Project(
            path=os.path.expanduser(proj['directory']),
            name=proj['name'],
            icon=proj.get('icon'),
            color=proj.get('color')
        ))

    options = [f"{p.icon or ''} {p.name}" for p in projects]

    # Usa fzf para seleccionar un proyecto
    try:
        # Lanza fzf con las opciones
        result = subprocess.run(
            ['fzf', '--prompt=Select a project: ', '--height=10%', '--layout=reverse', '--border'],
            input="\n".join(options),
            text=True,
            # capture_output=True
            stdout=subprocess.PIPE,
        )
        selected_option = result.stdout.strip()
        
        if selected_option:
            selected_index = options.index(selected_option)
            return projects[selected_index]
        else:
            print("No project selected.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to run fzf: {e}")
        return None

def open_in_kitty(project: Project):
    kitty_command = [
        'kitty', '@', 'launch',  # Abre una nueva ventana en Kitty
        '--type=overlay-main',  # Establece donde inciar el proceso [os-window, overlay-main, tap, window]
        '--cwd', project.path,  # Establece el directorio de trabajo
        '--title', project.name,  # Opcional: Establece el título de la ventana
        '--copy-env',
        'nvim', project.path, 
        # '&'
    ]

    try:
        subprocess.run(kitty_command, check=True)
        # print(f"Opened Kitty session for project: {project.name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open Kitty session: {e}")

def open_in_gnome_terminal(project: Project):
    command = ['gnome-terminal',
    '--',
    'nvim', project.path]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to open Kitty session: {e}")
