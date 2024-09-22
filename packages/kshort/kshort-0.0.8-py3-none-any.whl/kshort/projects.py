import os
import json
from kshort.project import Project

CACHE_FILE = os.path.expanduser("~/.config/projects_manager.json")

def get_projects():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            data = json.load(file)
            return {v['name']: Project(v['directory'], v['name'], None, v['icon'], v['color']) for v in data['projects']}
    return {}

def save_projects(projects):
    with open(CACHE_FILE, 'w') as file:
        json.dump({k: v.__dict__ for k, v in projects.items()}, file)

def remove_item(key):
    projects = get_projects()
    projects.pop(key, None)
    save_projects(projects)

def remove_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
