import json
import os
from typing import List, Optional

class ProjectConfig:
    def __init__(self, name: str, directory: str, icon: Optional[str] = None, color: Optional[str] = None):
        self.name = name
        self.directory = directory
        self.icon = icon
        self.color = color

    def __repr__(self):
        return f"ProjectConfig(name={self.name}, directory={self.directory}, icon={self.icon}, color={self.color})"

class Config:
    def __init__(self, directories: List[ProjectConfig], projects: List[ProjectConfig]):
        self.directories = directories
        self.projects = projects

    @staticmethod
    def load(path: str) -> 'Config':
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            print(f"Config file not found. Creating new file at {path}")
            default_config = {"directories": [], "projects": []}
            with open(path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return Config(directories=[], projects=[])

        with open(path, 'r') as f:
            try:
                data = json.load(f)
                directories = [ProjectConfig(**item) for item in data.get('directories', [])]
                projects = [ProjectConfig(**item) for item in data.get('projects', [])]
                return Config(directories=directories, projects=projects)
            except json.JSONDecodeError:
                print("Error decoding JSON from config file.")
                return Config(directories=[], projects=[])
            except ValueError as e:
                print(f"Config file error: {e}")
                return Config(directories=[], projects=[])

