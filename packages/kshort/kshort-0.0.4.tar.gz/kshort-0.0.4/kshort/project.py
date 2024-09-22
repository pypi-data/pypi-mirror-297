import os
import json

class Project:
    def __init__(self, path, name, group=None, icon=None, color=None):
        self.path = path
        self.name = name
        self.group = group
        self.icon = icon
        self.color = color

    def session_name(self):
        return f"[{self.group or ''}] {self.name.replace('.', '_')}"

    def kitty_display(self):
        if self.color:
            return f"#{self.color} {self.icon or ''} {self.name.replace('.', '_')}"
        return f"{self.icon or ''} {self.name.replace('.', '_')}"

    def __str__(self):
        return self.kitty_display()

    def get_command(self):
        config_path = os.path.join(self.path, ".projects_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data.get('cmd', 'kitty')
        return 'kitty'

