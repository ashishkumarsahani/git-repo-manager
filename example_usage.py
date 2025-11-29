#!/usr/bin/env python3
"""
Example usage of Git Repository Manager
This script demonstrates common use cases for the GitRepoManager class.
"""

from git_manager import GitRepoManager
import os
import time


def example_1_clone_repository():
    """Example 1: Clone a repository"""
    print("\n=== Example 1: Clone Repository ===")

    manager = GitRepoManager('config.yaml')

    # Clone the repository
    success = manager.clone_repository()

    if success:
        print("Repository cloned successfully!")
    else:
        print("Failed to clone repository")


def example_2_commit_and_push():
    """Example 2: Commit and push changes"""
    print("\n=== Example 2: Commit and Push Changes ===")

    manager = GitRepoManager('config.yaml')

    # Ensure repository exists
    if not os.path.exists(manager.target_dir):
        print("Repository not found, cloning first...")
        manager.clone_repository()

    # Create a sample file in the repository
    sample_file = os.path.join(manager.target_dir, 'example.txt')
    with open(sample_file, 'w') as f:
        f.write(f"This file was created at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Created sample file: {sample_file}")

    # Commit the changes
    commit_success = manager.commit_changes("Add example.txt file")

    if commit_success:
        print("Changes committed successfully!")

        # Push to remote
        push_success = manager.push_changes()

        if push_success:
            print("Changes pushed to remote successfully!")
        else:
            print("Failed to push changes")
    else:
        print("Failed to commit changes")


def example_3_pull_latest():
    """Example 3: Pull latest changes"""
    print("\n=== Example 3: Pull Latest Changes ===")

    manager = GitRepoManager('config.yaml')

    # Pull latest changes
    success = manager.pull_changes()

    if success:
        print("Successfully pulled latest changes!")
    else:
        print("Failed to pull changes")


def example_4_check_status():
    """Example 4: Check repository status"""
    print("\n=== Example 4: Check Repository Status ===")

    manager = GitRepoManager('config.yaml')

    # Get status
    status = manager.get_status()

    if status:
        print("Repository Status:")
        print(status)
    else:
        print("Failed to get status")


def example_5_full_workflow():
    """Example 5: Complete workflow - pull, modify, commit, push"""
    print("\n=== Example 5: Complete Workflow ===")

    manager = GitRepoManager('config.yaml')

    # Step 1: Ensure repository is cloned
    if not os.path.exists(manager.target_dir):
        print("Cloning repository...")
        if not manager.clone_repository():
            print("Failed to clone, exiting")
            return

    # Step 2: Pull latest changes
    print("Pulling latest changes...")
    if not manager.pull_changes():
        print("Failed to pull, continuing anyway...")

    # Step 3: Make changes
    print("Making changes to repository...")
    workflow_file = os.path.join(manager.target_dir, 'workflow_example.txt')
    with open(workflow_file, 'a') as f:
        f.write(f"Workflow executed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Step 4: Commit changes
    print("Committing changes...")
    if not manager.commit_changes("Update workflow example"):
        print("Failed to commit, exiting")
        return

    # Step 5: Push changes
    print("Pushing changes...")
    if manager.push_changes():
        print("Workflow completed successfully!")
    else:
        print("Failed to push changes")


def main():
    """Main function to run examples"""
    print("Git Repository Manager - Usage Examples")
    print("=" * 50)

    # You can uncomment the examples you want to run:

    # Example 1: Clone repository
    # example_1_clone_repository()

    # Example 2: Commit and push changes
    # example_2_commit_and_push()

    # Example 3: Pull latest changes
    # example_3_pull_latest()

    # Example 4: Check repository status
    # example_4_check_status()

    # Example 5: Full workflow
    # example_5_full_workflow()

    print("\nTo run examples, uncomment the desired example in the main() function")
    print("Make sure you have configured config.yaml before running!")


if __name__ == "__main__":
    main()
