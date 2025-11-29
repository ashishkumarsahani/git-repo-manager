# Quick Start Guide

Get started with Git Repository Manager in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Create Configuration File

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` with your details:

```yaml
repository:
  url: "https://github.com/YOUR_USERNAME/YOUR_REPO.git"
  target_directory: "./my_repo"
  branch: "main"

credentials:
  username: "YOUR_USERNAME"
  password: "YOUR_PERSONAL_ACCESS_TOKEN"

git_user:
  name: "Your Name"
  email: "your.email@example.com"
```

## Step 3: Clone Your Repository

```bash
python git_manager.py --clone
```

## Step 4: Make Changes and Commit

After modifying files in your repository:

```bash
python git_manager.py --commit "Your commit message" --push
```

## That's it!

You now have a working Git repository manager. For more advanced usage, check out:

- `README.md` - Full documentation
- `example_usage.py` - Python API examples
- `git_manager.py` - The main module with detailed docstrings

## Common Commands

```bash
# Check repository status
python git_manager.py --status

# Pull latest changes
python git_manager.py --pull

# Commit without pushing
python git_manager.py --commit "My changes"

# Push previously committed changes
python git_manager.py --push

# Force re-clone (removes existing directory)
python git_manager.py --force-clone
```

## Getting Your Personal Access Token

### GitHub
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`
4. Copy and paste into `config.yaml` as the password

### GitLab
1. Go to: https://gitlab.com/-/profile/personal_access_tokens
2. Create token with `read_repository` and `write_repository` scopes
3. Copy and paste into `config.yaml` as the password

## Troubleshooting

**Problem:** Authentication fails
**Solution:** Ensure you're using a Personal Access Token, not your account password

**Problem:** "No git repository found"
**Solution:** Run `--clone` first to clone the repository

**Problem:** "Directory exists but is not a git repository"
**Solution:** Use `--force-clone` to remove and re-clone

Need more help? Check the full `README.md` file.
