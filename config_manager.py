import os
import json
from pathlib import Path

CONFIG_FILE = Path.home() / '.git_auto_pusher.json'


def load_config():
    """Load saved configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'recent_repos': []}


def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def add_recent_repo(repo_path):
    """Add repository to recent list"""
    config = load_config()
    repo_path = os.path.abspath(repo_path)

    if repo_path in config['recent_repos']:
        config['recent_repos'].remove(repo_path)

    config['recent_repos'].insert(0, repo_path)
    save_config(config)
