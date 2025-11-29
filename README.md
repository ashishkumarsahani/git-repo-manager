# Git Repository Manager

A Python tool to manage Git repositories with support for cloning, committing, and pushing changes using credentials stored in a configuration file.

## Features

- Clone Git repositories with authentication
- Commit changes with customizable messages
- Push changes to remote repositories
- Pull latest changes from remote
- Check repository status
- Credentials stored securely in a config file
- Support for both HTTPS and SSH authentication
- Automatic git user configuration for commits
- Command-line interface for easy automation

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Create your configuration file:

```bash
cp config.example.yaml config.yaml
```

3. Edit `config.yaml` with your repository details and credentials.

## Configuration

The `config.yaml` file contains all necessary settings:

```yaml
repository:
  url: "https://github.com/username/repository.git"
  target_directory: "./cloned_repo"
  branch: "main"

credentials:
  username: "your_username"
  password: "your_personal_access_token"

git_user:
  name: "Your Name"
  email: "your.email@example.com"

commit_settings:
  auto_add_all: true
  default_commit_message: "Auto commit"
```

### Important Security Notes

- **Never commit `config.yaml` to version control** - it contains sensitive credentials
- Use Personal Access Tokens instead of passwords for GitHub/GitLab
- The `config.example.yaml` is safe to commit as it contains no real credentials

## Usage

### Command Line Interface

```bash
# Clone a repository
python git_manager.py --clone

# Force clone (removes existing directory)
python git_manager.py --force-clone

# Commit changes
python git_manager.py --commit "Your commit message"

# Push changes
python git_manager.py --push

# Pull changes
python git_manager.py --pull

# Check status
python git_manager.py --status

# Combine operations
python git_manager.py --commit "Update files" --push
```

### Python API

```python
from git_manager import GitRepoManager

# Initialize the manager
manager = GitRepoManager('config.yaml')

# Clone repository
manager.clone_repository()

# Make some changes to files in the repository...

# Commit changes
manager.commit_changes("Added new feature")

# Push to remote
manager.push_changes()

# Pull latest changes
manager.pull_changes()

# Check status
status = manager.get_status()
print(status)
```

## API Reference

### GitRepoManager

Main class for managing Git repository operations.

#### `__init__(config_path: str = "config.yaml")`

Initialize the manager with a configuration file.

#### `clone_repository(force: bool = False) -> bool`

Clone the repository to the target directory.

- `force`: If True, removes existing directory before cloning
- Returns: True if successful, False otherwise

#### `commit_changes(message: str, add_all: bool = None) -> bool`

Commit changes to the repository.

- `message`: Commit message
- `add_all`: If True, adds all changes before commit. If None, uses config default
- Returns: True if successful, False otherwise

#### `push_changes(remote: str = "origin", branch: str = None) -> bool`

Push changes to remote repository.

- `remote`: Name of the remote (default: "origin")
- `branch`: Branch to push to (default: current branch)
- Returns: True if successful, False otherwise

#### `pull_changes(remote: str = "origin", branch: str = None) -> bool`

Pull changes from remote repository.

- `remote`: Name of the remote (default: "origin")
- `branch`: Branch to pull from (default: current branch)
- Returns: True if successful, False otherwise

#### `get_status() -> Optional[str]`

Get the current repository status.

- Returns: Status string or None if repo not loaded

## Example Workflows

### Workflow 1: Clone and Setup

```python
from git_manager import GitRepoManager

manager = GitRepoManager()
manager.clone_repository()
```

### Workflow 2: Update and Push Changes

```python
from git_manager import GitRepoManager
import os

# Initialize manager
manager = GitRepoManager()

# Ensure repo is cloned
if not os.path.exists(manager.target_dir):
    manager.clone_repository()

# Make changes to files
# ... your code to modify files ...

# Commit and push
manager.commit_changes("Updated configuration files")
manager.push_changes()
```

### Workflow 3: Sync Before Making Changes

```python
from git_manager import GitRepoManager

manager = GitRepoManager()

# Pull latest changes first
manager.pull_changes()

# Make your changes
# ... your code ...

# Commit and push
manager.commit_changes("My changes")
manager.push_changes()
```

## Generating Personal Access Tokens

### GitHub

1. Go to Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (for private repos) or `public_repo` (for public repos)
4. Copy the token and use it as the password in `config.yaml`

### GitLab

1. Go to Preferences → Access Tokens
2. Create a token with `read_repository` and `write_repository` scopes
3. Copy the token and use it as the password in `config.yaml`

### Bitbucket

1. Go to Personal settings → App passwords
2. Create an app password with repository read/write permissions
3. Copy the password and use it in `config.yaml`

## Troubleshooting

### Authentication Fails

- Ensure your Personal Access Token has the correct permissions
- Check that username and token are correct in `config.yaml`
- For GitHub, make sure you're using a Personal Access Token, not your account password

### Repository Already Exists

- Use `--force-clone` to remove and re-clone
- Or manually delete the target directory

### Permission Denied

- Check file permissions on the target directory
- Ensure your credentials have push access to the repository

## Security Best Practices

1. Never commit `config.yaml` to version control
2. Add `config.yaml` to `.gitignore`
3. Use Personal Access Tokens with minimal required permissions
4. Rotate tokens regularly
5. Use environment variables for CI/CD instead of config files

## License

This tool is provided as-is for educational and development purposes.
