#!/usr/bin/env python3
"""
Git Repository Manager
A Python tool to clone, commit, and push to Git repositories using credentials from a config file.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GitRepoManager:
    """Manages Git repository operations including clone, commit, and push."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the Git Repository Manager.

        Args:
            config_path: Path to the configuration YAML file
        """
        self.config = self._load_config(config_path)
        self.repo: Optional[Repo] = None
        self.repo_url = self.config['repository']['url']
        self.target_dir = self.config['repository']['target_directory']
        self.branch = self.config['repository'].get('branch', 'main')

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to the config file

        Returns:
            Dictionary containing configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found: {config_path}\n"
                f"Please copy config.example.yaml to config.yaml and fill in your details."
            )

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        logger.info(f"Configuration loaded from {config_path}")
        return config

    def _get_authenticated_url(self) -> str:
        """
        Create an authenticated Git URL with credentials.

        Returns:
            URL with embedded credentials
        """
        credentials = self.config.get('credentials', {})
        username = credentials.get('username')
        password = credentials.get('password')

        if not username or not password:
            logger.warning("No credentials found in config, using URL as-is")
            return self.repo_url

        # Parse the URL and inject credentials
        if self.repo_url.startswith('https://'):
            # Remove https:// prefix
            url_without_protocol = self.repo_url[8:]
            # Create authenticated URL
            authenticated_url = f"https://{username}:{password}@{url_without_protocol}"
            return authenticated_url
        elif self.repo_url.startswith('http://'):
            # Remove http:// prefix
            url_without_protocol = self.repo_url[7:]
            # Create authenticated URL
            authenticated_url = f"http://{username}:{password}@{url_without_protocol}"
            return authenticated_url
        else:
            # For SSH URLs, return as-is
            logger.info("Using SSH URL, credentials from config will be ignored")
            return self.repo_url

    def clone_repository(self, force: bool = False) -> bool:
        """
        Clone the repository to the target directory.

        Args:
            force: If True, remove existing directory before cloning

        Returns:
            True if successful, False otherwise
        """
        try:
            target_path = Path(self.target_dir)

            # Check if directory already exists
            if target_path.exists():
                if force:
                    logger.warning(f"Removing existing directory: {self.target_dir}")
                    import shutil
                    shutil.rmtree(self.target_dir)
                else:
                    # Try to open existing repo
                    try:
                        self.repo = Repo(self.target_dir)
                        logger.info(f"Repository already exists at {self.target_dir}")
                        return True
                    except InvalidGitRepositoryError:
                        logger.error(
                            f"Directory exists but is not a git repository: {self.target_dir}\n"
                            f"Use force=True to remove and re-clone"
                        )
                        return False

            # Clone the repository
            logger.info(f"Cloning repository from {self.repo_url}")
            authenticated_url = self._get_authenticated_url()

            self.repo = Repo.clone_from(
                authenticated_url,
                self.target_dir,
                branch=self.branch
            )

            # Configure git user for commits
            self._configure_git_user()

            logger.info(f"Repository cloned successfully to {self.target_dir}")
            return True

        except GitCommandError as e:
            logger.error(f"Git command failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return False

    def _configure_git_user(self):
        """Configure git user name and email from config."""
        if not self.repo:
            return

        git_user = self.config.get('git_user', {})
        name = git_user.get('name')
        email = git_user.get('email')

        if name:
            self.repo.config_writer().set_value("user", "name", name).release()
            logger.info(f"Configured git user name: {name}")

        if email:
            self.repo.config_writer().set_value("user", "email", email).release()
            logger.info(f"Configured git user email: {email}")

    def _ensure_repo_loaded(self) -> bool:
        """
        Ensure repository is loaded.

        Returns:
            True if repo is loaded, False otherwise
        """
        if self.repo is None:
            try:
                self.repo = Repo(self.target_dir)
                self._configure_git_user()
                return True
            except InvalidGitRepositoryError:
                logger.error(
                    f"No git repository found at {self.target_dir}\n"
                    f"Please clone the repository first using clone_repository()"
                )
                return False
        return True

    def commit_changes(self, message: str, add_all: bool = None) -> bool:
        """
        Commit changes to the repository.

        Args:
            message: Commit message
            add_all: If True, add all changes before commit.
                    If None, use config default.

        Returns:
            True if successful, False otherwise
        """
        if not self._ensure_repo_loaded():
            return False

        try:
            # Determine if we should add all changes
            if add_all is None:
                add_all = self.config.get('commit_settings', {}).get('auto_add_all', True)

            # Add changes
            if add_all:
                self.repo.git.add(A=True)
                logger.info("Added all changes to staging area")

            # Check if there are changes to commit
            if not self.repo.is_dirty() and not self.repo.untracked_files:
                logger.warning("No changes to commit")
                return True

            # Commit changes
            commit = self.repo.index.commit(message)
            logger.info(f"Changes committed successfully: {commit.hexsha[:7]} - {message}")
            return True

        except GitCommandError as e:
            logger.error(f"Git commit failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to commit changes: {e}")
            return False

    def push_changes(self, remote: str = "origin", branch: str = None) -> bool:
        """
        Push changes to remote repository.

        Args:
            remote: Name of the remote (default: origin)
            branch: Branch to push to (default: current branch or config branch)

        Returns:
            True if successful, False otherwise
        """
        if not self._ensure_repo_loaded():
            return False

        try:
            # Determine branch
            if branch is None:
                branch = self.repo.active_branch.name

            # Update remote URL with credentials if needed
            authenticated_url = self._get_authenticated_url()

            # Get or create remote
            if remote in [r.name for r in self.repo.remotes]:
                remote_obj = self.repo.remote(remote)
                # Update URL with credentials
                remote_obj.set_url(authenticated_url)
            else:
                remote_obj = self.repo.create_remote(remote, authenticated_url)

            # Push changes
            logger.info(f"Pushing changes to {remote}/{branch}")
            push_info = remote_obj.push(branch)

            # Check push result
            if push_info and push_info[0].flags & push_info[0].ERROR:
                logger.error(f"Push failed: {push_info[0].summary}")
                return False

            logger.info("Changes pushed successfully")
            return True

        except GitCommandError as e:
            logger.error(f"Git push failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to push changes: {e}")
            return False

    def get_status(self) -> Optional[str]:
        """
        Get the current repository status.

        Returns:
            Status string or None if repo not loaded
        """
        if not self._ensure_repo_loaded():
            return None

        try:
            status = self.repo.git.status()
            return status
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return None

    def pull_changes(self, remote: str = "origin", branch: str = None) -> bool:
        """
        Pull changes from remote repository.

        Args:
            remote: Name of the remote (default: origin)
            branch: Branch to pull from (default: current branch)

        Returns:
            True if successful, False otherwise
        """
        if not self._ensure_repo_loaded():
            return False

        try:
            if branch is None:
                branch = self.repo.active_branch.name

            logger.info(f"Pulling changes from {remote}/{branch}")
            remote_obj = self.repo.remote(remote)
            remote_obj.pull(branch)

            logger.info("Changes pulled successfully")
            return True

        except GitCommandError as e:
            logger.error(f"Git pull failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to pull changes: {e}")
            return False


def main():
    """Main function demonstrating usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Git Repository Manager')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--clone', action='store_true', help='Clone the repository')
    parser.add_argument('--force-clone', action='store_true', help='Force clone (remove existing)')
    parser.add_argument('--commit', type=str, help='Commit with message')
    parser.add_argument('--push', action='store_true', help='Push changes')
    parser.add_argument('--pull', action='store_true', help='Pull changes')
    parser.add_argument('--status', action='store_true', help='Show repository status')

    args = parser.parse_args()

    try:
        # Initialize manager
        manager = GitRepoManager(args.config)

        # Execute commands
        if args.clone or args.force_clone:
            success = manager.clone_repository(force=args.force_clone)
            if not success:
                sys.exit(1)

        if args.pull:
            success = manager.pull_changes()
            if not success:
                sys.exit(1)

        if args.commit:
            success = manager.commit_changes(args.commit)
            if not success:
                sys.exit(1)

        if args.push:
            success = manager.push_changes()
            if not success:
                sys.exit(1)

        if args.status:
            status = manager.get_status()
            if status:
                print("\nRepository Status:")
                print(status)

        # If no arguments, show help
        if not any([args.clone, args.force_clone, args.commit, args.push, args.pull, args.status]):
            parser.print_help()

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
