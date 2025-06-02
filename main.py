#!/usr/bin/env python3
"""
Git Auto-Pusher
A tool to automatically commit and push changes to a git repository
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

# Import local modules
from git_operations import get_repo_status, commit_and_push
from macos_utils import send_notification, get_credentials, set_credentials

# Configuration management
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


class GitAutoPusher:
    """Main class for the Git Auto-Pusher application"""

    def __init__(self, repo_path=None, watch_interval=30):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.watch_interval = watch_interval
        self.running = False
        add_recent_repo(self.repo_path)  # Save repo path to config

    def setup_credentials(self):
        """Setup GitHub credentials if not already stored"""
        username, token = get_credentials()
        if not username or not token:
            print("GitHub credentials not found. Please set them up:")
            username = input("GitHub username: ").strip()
            token = input("GitHub personal access token: ").strip()
            if username and token:
                set_credentials(username, token)
                print("Credentials saved to keychain.")
                return True
            else:
                print("Invalid credentials provided.")
                return False
        print(f"Using stored credentials for user: {username}")
        return True

    def check_and_push_changes(self):
        """Check for changes and push if any are found"""
        try:
            status = get_repo_status(self.repo_path)
            if not status['is_repo']:
                error_msg = f"{self.repo_path} is not a git repository"
                print(error_msg)
                send_notification("Git Auto-Pusher Error", error_msg)
                return False

            if status['has_changes']:
                print("Changes detected. Committing and pushing...")
                commit_message = f"Auto-commit: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                success = commit_and_push(self.repo_path, commit_message)
                if success:
                    message = f"Successfully pushed changes to {self.repo_path.name}"
                    print(message)
                    send_notification("Git Auto-Pusher", message)
                    return True
                else:
                    error_msg = "Failed to push changes"
                    print(error_msg)
                    send_notification("Git Auto-Pusher Error", error_msg)
                    return False
            else:
                print("No changes detected.")
                return True

        except Exception as e:
            error_msg = f"Error during git operations: {str(e)}"
            print(error_msg)
            send_notification("Git Auto-Pusher Error", error_msg)
            return False

    def watch_mode(self):
        """Continuously monitor the repository for changes"""
        print(f"Starting watch mode for repository: {self.repo_path}")
        print(f"Checking for changes every {self.watch_interval} seconds")
        print("Press Ctrl+C to stop")
        self.running = True
        try:
            while self.running:
                self.check_and_push_changes()
                time.sleep(self.watch_interval)
        except KeyboardInterrupt:
            print("\nStopping Git Auto-Pusher...")
            self.running = False

    def run_once(self):
        """Run a single check and push operation"""
        print(f"Checking repository: {self.repo_path}")
        return self.check_and_push_changes()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Automatically commit and push git changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run once in current directory
  python main.py --watch           # Watch current directory
  python main.py --path /path/to/repo --watch --interval 60
  python main.py --setup-credentials
        """
    )
    parser.add_argument(
        "--path", "-p",
        type=str,
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Continuously watch for changes"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=30,
        help="Check interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--setup-credentials",
        action="store_true",
        help="Setup GitHub credentials"
    )
    args = parser.parse_args()

    try:
        pusher = GitAutoPusher(repo_path=args.path,
                               watch_interval=args.interval)
        if not get_repo_status(pusher.repo_path)['is_repo']:
            print(f"Error: {pusher.repo_path} is not a git repository")
            sys.exit(1)

        if args.setup_credentials:
            if pusher.setup_credentials():
                print("Credentials setup completed.")
            else:
                print("Credentials setup failed.")
                sys.exit(1)
            return

        if not pusher.setup_credentials():
            print("Cannot proceed without valid credentials.")
            sys.exit(1)

        if args.watch:
            pusher.watch_mode()
        else:
            success = pusher.run_once()
            sys.exit(0 if success else 1)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
